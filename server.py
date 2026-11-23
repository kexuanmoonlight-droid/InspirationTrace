"""InspirationTrace V4: local-only, multi-turn creative chat + cited candidate-source lookup.
No public hosting; keep API key in local environment, never in browser.
"""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from pathlib import Path
import json, os, re
from offline_modes import mock_chat, demo_evidence, ollama_chat, ollama_available

ROOT=Path(__file__).resolve().parent
HOST='127.0.0.1'
PORT=int(os.getenv('PORT','8765'))
GEN_MODEL=os.getenv('INSPIRATIONTRACE_MODEL','gpt-4.1-mini')
SEARCH_MODEL=os.getenv('INSPIRATIONTRACE_SEARCH_MODEL','gpt-5.6')
DEFAULT_MODE=os.getenv('INSPIRATIONTRACE_MODE','demo').lower()

SYSTEM='''You are InspirationTrace, a flexible, imaginative creative-writing conversation partner, not a rigid story template. Follow the author's language, genre, mood, scope and requests. A user might ask an open question, brainstorm, or ask for an outline. Reply naturally. For initial story ideas or explicit rewrite requests, build a coherent, original multi-section story outline. For other conversation respond without forcing a rewrite. When revising use the active prior outline as the foundation, integrating new ideas causally while respecting established choices unless the author wants changes. Do NOT copy wording or identifiable expressive elements from other authors. Never fabricate citations, sources, similarity scores or imply that generated fiction has confirmed provenance. You have no knowledge of model training examples. Return only JSON with keys: message (natural conversational reply), update_outline (boolean), outline (object with title and sections each containing heading and text, if update_outline true; otherwise null), change_summary (short string). Do not force every story into one genre or a standard seven-beat template. Generate substantive connected story content in the author's language.'''

def reply(handler,status,data):
    b=json.dumps(data,ensure_ascii=False).encode('utf-8')
    handler.send_response(status);handler.send_header('Content-Type','application/json; charset=utf-8');handler.send_header('Cache-Control','no-store');handler.send_header('Content-Length',str(len(b)));handler.end_headers();handler.wfile.write(b)

def provider(endpoint,body):
    key=os.getenv('OPENAI_API_KEY','').strip()
    if not key:raise RuntimeError('OPENAI_API_KEY is not set. Set the key in your local terminal before starting server.py.')
    req=Request('https://api.openai.com/v1/'+endpoint, data=json.dumps(body,ensure_ascii=False).encode('utf-8'),headers={'Content-Type':'application/json','Authorization':'Bearer '+key},method='POST')
    try:
        with urlopen(req,timeout=110) as r:return json.loads(r.read().decode('utf-8'))
    except HTTPError as e:
        detail=e.read().decode('utf-8','replace')[:450]
        raise RuntimeError('Model service HTTP '+str(e.code)+'：'+detail)
    except URLError as e:raise RuntimeError('Could not connect to the model service: '+str(e.reason))

def valid_outline(out):
    if not isinstance(out,dict) or not isinstance(out.get('sections'),list):raise ValueError('The model did not return a valid story outline.')
    sections=[]
    for row in out['sections'][:12]:
        if not isinstance(row,dict):continue
        head=str(row.get('heading','')).strip()[:160];body=str(row.get('text','')).strip()[:7000]
        if head and body:sections.append({'heading':head,'text':body})
    if not sections:raise ValueError('The model returned an empty outline.')
    result={'title':str(out.get('title','Untitled story'))[:180],'sections':sections}
    if out.get('demo_scenario') in ('memory','mystery','fantasy'):
        result['demo_scenario']=out['demo_scenario'];result['demo_stage']=int(out.get('demo_stage',1))
    return result

def chat(payload):
    message=str(payload.get('message','')).strip()
    if not message or len(message)>12000:raise ValueError('Enter a creative-writing message of 1–12,000 characters.')
    current=payload.get('currentOutline')
    if current is not None: current=valid_outline(current)
    history=payload.get('history') or []
    if not isinstance(history,list):history=[]
    clean_history=[]
    for h in history[-18:]:
        if isinstance(h,dict) and h.get('role') in ('user','assistant'):
            clean_history.append({'role':h['role'],'text':str(h.get('text',''))[:3500]})
    selected=payload.get('selectedReferences') or []
    if not isinstance(selected,list):selected=[]
    refs=[{'title':str(s.get('title',''))[:120],'url':str(s.get('url',''))[:400]} for s in selected[:12] if isinstance(s,dict)]
    context={'current_outline':current,'recent_conversation':clean_history,'author_selected_reference_records':refs,'new_message':message,'rule':'If author requests a modification to current outline, revise the WHOLE outline in context. Do not merely append the new instruction. If author is asking a question instead, converse naturally without forcing a new outline. Reference selections are optional inspiration, not proof model used those sources.'}
    raw=provider('chat/completions',{'model':GEN_MODEL,'temperature':0.8,'response_format':{'type':'json_object'},'messages':[{'role':'system','content':SYSTEM},{'role':'user','content':json.dumps(context,ensure_ascii=False)}]})
    try:
        obj=json.loads(raw['choices'][0]['message']['content']); update=obj.get('update_outline') is True
        outline=valid_outline(obj.get('outline')) if update else None
        return {'message':str(obj.get('message',''))[:5000] or ('Story outline updated.' if update else 'We can explore this further.'),'updated':update,'outline':outline,'change_summary':str(obj.get('change_summary',''))[:1000]}
    except (ValueError,KeyError,IndexError,TypeError,json.JSONDecodeError) as e:raise RuntimeError('Could not parse the model response: '+str(e))

def candidate_sources(payload):
    """Only return source URLs present in provider web-search citation annotations.
    Search results are candidate comparisons, never proven model influences or full-text matches.
    """
    outline=valid_outline(payload.get('outline'))
    lines='\n'.join(f'SECTION {i+1}: {s["heading"]}: {s["text"][:1100]}' for i,s in enumerate(outline['sections'][:8]))
    prompt=('Search publicly available descriptions of EXISTING published fiction that may share a specific narrative theme, setting, or plot device with the outline below. Use web search; cite real publisher, author, library, or reputable award/book pages. Do not invent titles, URLs or claim copying or training provenance. Return up to 5 concise comparison items, each starting exactly with "SECTION N:" where N is the most relevant section number (1-based), then state shared theme and major differences and cite the supporting page. If evidence is weak, say so; fewer items are preferable. Do not label a work as an inspiration source of the model.\n\n'+lines)
    raw=provider('responses',{'model':SEARCH_MODEL,'tools':[{'type':'web_search','search_context_size':'medium'}],'input':prompt,'max_output_tokens':1500})
    cards=[];seen=set();textout=''
    for output in raw.get('output',[]):
        if output.get('type')!='message':continue
        for content in output.get('content',[]):
            if content.get('type')!='output_text':continue
            text=content.get('text','');textout+=text+'\n'
            for annotation in content.get('annotations',[]):
                if annotation.get('type')!='url_citation':continue
                node=annotation.get('url_citation',annotation)
                url=str(node.get('url',''))
                if not url.startswith('https://') or url in seen:continue
                seen.add(url)
                start=node.get('start_index',0)
                if not isinstance(start,int) or start<0 or start>len(text):start=0
                before=text[:start];section_matches=list(re.finditer(r'SECTION\s+(\d+)\s*:',before,re.I))
                section=int(section_matches[-1].group(1))-1 if section_matches else None
                if section is not None and not (0<=section<len(outline['sections'])):section=None
                chunk=before[section_matches[-1].end():].strip() if section_matches else ''
                chunk=re.sub(r'\s+',' ',chunk)[-650:]
                cards.append({'id':'src-'+str(len(cards)+1),'title':str(node.get('title','Source page'))[:180],'url':url,'sectionIndex':section,'comparison':chunk[:400] or 'Please open the original source and assess similarities and differences.','kind':'potentially_similar','reviewed':False,'selected':False})
    return {'records':cards[:8],'has_search_citations':bool(cards),'notice':('Only clickable URLs returned by the search tool are displayed. Candidate works are not verified model sources, and description-level comparisons do not establish plagiarism or full-text similarity.' if cards else 'Search returned no verifiable citation links; no similarity finding or inline annotations are shown.'),'rawSummary':textout[:2500]}

class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(ROOT),**kwargs)
    def do_GET(self):
        if self.path=='/api/status':return reply(self,200,{'configured':bool(os.getenv('OPENAI_API_KEY')),'model':GEN_MODEL,'searchModel':SEARCH_MODEL,'search':'provider_web_search_when_requested','mode':DEFAULT_MODE,'ollamaModels':ollama_available()})
        return super().do_GET()
    def do_POST(self):
        if self.path not in ('/api/chat','/api/evidence'):return reply(self,404,{'error':'Not found'})
        try:
            size=int(self.headers.get('Content-Length','0'))
            if not 0<size<=200000:raise ValueError('Request body is empty or too long.')
            payload=json.loads(self.rfile.read(size))
            if not isinstance(payload,dict):raise ValueError('Request body must be a JSON object.')
            mode=str(payload.get('mode',DEFAULT_MODE)).lower()
            if mode not in ('demo','ollama','openai'):raise ValueError('Unknown run mode.')
            if self.path=='/api/chat':
                data=mock_chat(payload) if mode=='demo' else (ollama_chat(payload,SYSTEM,valid_outline) if mode=='ollama' else chat(payload))
            else:
                data=demo_evidence(payload) if mode=='demo' else ({'records':[],'notice':'Ollama supports local generation only; reliable source retrieval is unavailable. Do not treat unverified links as evidence.'} if mode=='ollama' else candidate_sources(payload))
            return reply(self,200,data)
        except ValueError as e:return reply(self,400,{'error':str(e)})
        except (RuntimeError,KeyError,TypeError) as e:return reply(self,503,{'error':str(e)})
        except Exception as e:return reply(self,500,{'error':'Server error: '+type(e).__name__})
    def log_message(self,*args):pass

if __name__=='__main__':
    print('InspirationTrace V5: http://'+HOST+':'+str(PORT),'Default mode:',DEFAULT_MODE,'Cloud generation:',GEN_MODEL,'Cloud search:',SEARCH_MODEL)
    ThreadingHTTPServer((HOST,PORT),Handler).serve_forever()
