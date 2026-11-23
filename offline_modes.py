"""Transparent offline scripted demo and optional local Ollama adapter.
No synthetic facts or pretend verification. Standard library only.
"""
import json, os
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

MEMORY_URL = 'https://www.penguin.co.uk/books/429817/the-memory-police-by-yoko-ogawa/9781784700447'
PRIORY_URL = 'https://www.bloomsbury.com/uk/priory-of-the-orange-tree-9781408883358/'
HOBBIT_URL = 'https://www.harperreach.com/products/the-hobbit-j-r-r-tolkien-9780007458424/'

SCENARIOS = {
 'memory': {
   'label':'Memory Market — Source Review Demo',
   'trigger':['memory','memories','archive','记忆','失忆'],
   'title':'The Lost Ledger of the Memory Market',
   'sections':[
    {'heading':'Core premise','text':'In a coastal city, adults can voluntarily sell a chosen personal memory, but they cannot sell other people’s recollections of the same event. Every transaction is archived.'},
    {'heading':'Characters and goals','text':'Mara, an archivist, discovers that her father sold a memory of her childhood. She wants to know why it was so valuable and whom he was trying to protect.'},
    {'heading':'Central conflict','text':'Mara finds that transaction registers have been altered. Family members disagree about the same event, while the agency running the market refuses to release the original records.'},
    {'heading':'Reversal','text':'The memories were not simply erased: buyers used them to reconstruct a concealed collective disaster. Mara must choose between exposing the truth and protecting surviving relatives.'},
    {'heading':'Possible ending','text':'She exposes the fraudulent recordkeeping without revealing sellers’ private memories. The city begins debating the limits of memory trading.'}],
   'evidence':[{'id':'memory-1','title':'The Memory Police — Yoko Ogawa','url':MEMORY_URL,'sectionIndex':0,'comparison':'Manually curated thematic comparison: this novel explores disappearing memories and social relationships, while the demo story involves voluntary memory sales. The publisher page does not establish that any model used the novel as a source.','kind':'manually_curated','source':'Penguin · publisher book page','review_basis':'Publisher description (manually checked)'}]
 },
 'mystery': {
   'label':'Letters from Ten Years Ahead — Revision Demo',
   'trigger':['postman','postwoman','letter','ten years','邮递员','来信','十年后'],
   'title':'The Postmark from Ten Years Ahead',
   'sections':[
    {'heading':'Opening','text':'Lin, a small-town postal worker, receives a letter postmarked ten years in the future. It accurately describes a minor event that occurs the next day.'},
    {'heading':'Protagonist','text':'Lin prefers a quiet routine, but another letter forecasting a fire prompts an investigation into the sender.'},
    {'heading':'Central conflict','text':'Someone is using future letters to influence residents’ choices. Lin must decide whether changing one future might endanger another family.'},
    {'heading':'Development and reversal','text':'The letters come from several possible futures rather than a single destiny. Every intervention changes the next letter.'},
    {'heading':'Possible ending','text':'Lin publicly explains the pattern, giving townspeople control over their own decisions instead of allowing one anonymous sender to shape their lives.'}],
   'evidence':[]
 },
 'fantasy': {
   'label':'Fantasy Rescue — Three-Round Demo',
   'trigger':['princess','prince','dragon','fantasy','rescue','公主','王子','龙','奇幻'],
   'title':'A Rescue Across the Ashen Mountains',
   'sections':[
    {'heading':'Opening','text':'A remarkably strong princess who does not want to inherit the throne sets out to rescue a prince trapped in a mountain valley, determined to prove that rescue need not depend on an ancient royal prophecy.'},
    {'heading':'Character relationships','text':'The prince understands old maps but cannot fight well. The princess is decisive in action but knows little about the valley residents’ historic pact with the royal family. They must learn to trust one another.'},
    {'heading':'Conflict','text':'During the rescue, royal troops block the mountain road, afraid that the valley residents know about a betrayal by the royal family.'},
    {'heading':'Reversal','text':'The princess discovers that the apparent imprisonment is actually a political bargain: the prince chose to stay to protect the villagers.'},
    {'heading':'Ending direction','text':'They expose the old pact, reject a political marriage as the solution, and encourage both sides to renegotiate.'}],
   'evidence':[
    {'id':'fantasy-priory','title':'The Priory of the Orange Tree — Samantha Shannon','url':PRIORY_URL,'sectionIndex':2,'comparison':'Manually curated thematic comparison: the publisher description covers dragons, royalty and political power. V1 relates only to a broad royal-betrayal motif; V2–V3 include dragon politics. This does not establish identical events, textual overlap, or model provenance.','kind':'manually_curated','source':'Bloomsbury Publishing · publisher book page','review_basis':'Publisher description (manually checked)'},
    {'id':'fantasy-hobbit','title':'The Hobbit — J. R. R. Tolkien','url':HOBBIT_URL,'sectionIndex':0,'comparison':'Manually curated broad genre comparison (weak relevance): the publisher page describes an adventure featuring a dragon. The V1 link concerns only a general rescue/adventure motif; dragons enter the demo in V2–V3. No plot copying or textual similarity is implied.','kind':'manually_curated','source':'HarperCollins / HarperReach · official book page','review_basis':'Publisher description (manually checked)'}]
 }
}

def scenario_for(message,current=None):
    if current and current.get('demo_scenario') in SCENARIOS: return current['demo_scenario']
    text=message.lower()
    for name,s in SCENARIOS.items():
        if any(w in text for w in s['trigger']):return name
    return None

def mock_chat(payload):
    """Fixed, explicitly labelled scenario steps; unsupported input is never framed as AI understanding."""
    message=str(payload.get('message','')).strip()
    if not message: raise ValueError('Enter a message.')
    previous=payload.get('currentOutline')
    context=previous if isinstance(previous,dict) else None
    key=scenario_for(message,context)
    if not key:
        return {'message':'[SCRIPTED DEMO] This request does not match a prepared scene. Choose a demo scenario or switch to a working Ollama/OpenAI model.','updated':False,'outline':None,'change_summary':'','demo':True}
    script=SCENARIOS[key]
    if context is None:
        outline={'title':script['title'],'sections':[dict(x) for x in script['sections']],'demo_scenario':key,'demo_stage':1}
        return {'message':'[SCRIPTED RESPONSE] Loaded the first outline for “'+script['label']+'”. No AI model was called.','updated':True,'outline':outline,'change_summary':'Loaded a pre-written demonstration scenario','demo':True}
    stage=int(context.get('demo_stage',1))
    low=message.lower()
    if any(w in low for w in ['why','explain','discuss','question','do not update','don’t update','?', '？','讨论','解释','为什么','不更新','不要更新']):
        return {'message':'[SCRIPTED RESPONSE] The offline demo cannot interpret this open-ended question as a real model would. The outline is unchanged.','updated':False,'outline':None,'change_summary':'','demo':True}
    if key=='fantasy' and stage==1 and any(w in low for w in ['dragon','龙']):
        outline={'title':'The Ashen Mountains and the Last Dragon','sections':[
          {'heading':'Opening','text':'The strong princess sets out to rescue the prince. She discovers that an ancient dragon has awakened and that dragon hunters, not regular troops, have sealed the mountain paths.'},
          {'heading':'Characters and relationships','text':'The prince can interpret dragon speech; the princess protects the party. A young dragon mistakes her for someone who once saved it, becoming an unreliable but vital companion.'},
          {'heading':'Escalating conflict','text':'The kingdom seeks to seize dragonfire to control mountain resources. The princess must choose between rescuing the prince quickly and helping the dragons escape persecution.'},
          {'heading':'Main reversal','text':'The prince has stayed voluntarily to guard a dragon-egg sanctuary. The princess discovers that this rescue is entangled with a long-concealed pact between the kingdom and the dragons.'},
          {'heading':'Ending direction','text':'The princess, prince and dragons expose the deception, prevent a wider war and transform a personal rescue into an attempt to change political relations.'}], 'demo_scenario':key,'demo_stage':2}
        return {'message':'[SCRIPTED RESPONSE] Loaded the pre-written dragon revision. The dragon changes the central conflict. This is a fixed script, not unrestricted AI understanding.','updated':True,'outline':outline,'change_summary':'Scripted revision: dragons change the rescue, relationships and conflict','demo':True}
    if key=='fantasy' and stage==2 and ((('prince' in low or '王子' in low) and ('dragon' in low or '龙' in low)) or ('character' in low and 'relationship' in low) or ('人物' in low and '关系' in low)):
        outline={'title':'The Ashen Mountains: The Prince’s Secret Pact with the Dragons','sections':[
          {'heading':'Opening','text':'The princess ventures into the Ashen Mountains to find the prince, only to discover that he stayed voluntarily to nurse an injured young dragon. The princess must become a negotiator rather than simply a rescuer.'},
          {'heading':'Characters and relationships','text':'The prince secretly promised the dragon elders that he would protect the dragon-egg sanctuary. The hatchling trusts him as its guardian, while the princess initially views his promise as a betrayal of the kingdom. Their misunderstandings turn into an uneasy alliance.'},
          {'heading':'Escalating conflict','text':'The dragon hunters call the prince’s promise treason and demand that the princess hand him over. The dragons fear another human betrayal and insist the prince stay as a guarantee.'},
          {'heading':'Main reversal','text':'The princess learns that an earlier royal generation broke the pact. The prince has sacrificed his freedom to delay dragon retaliation, prompting her to turn a private rescue into public negotiations.'},
          {'heading':'Ending direction','text':'The princess reveals the old pact, the prince sets clear limits to his promise, and the dragon elders agree to oversee a new truce. Their roles shift from protector and protected to shared responsibility.'}], 'demo_scenario':key,'demo_stage':3}
        return {'message':'[SCRIPTED RESPONSE] Loaded the prepared third-round relationship revision. The prince–dragon bond now shapes the rescue, conflict and ending. This is not an open-ended AI response.','updated':True,'outline':outline,'change_summary':'Scripted third round: the prince–dragon relationship changes motivation, conflict and resolution','demo':True}
    if key=='mystery' and stage==1 and any(w in low for w in ['sister','family','妹妹','姐姐','家人']):
        sections=[dict(x) for x in context['sections']]
        sections[1]['text']='Lin investigates the letters with an estranged sister, who still resents a missed urgent message years earlier.'
        sections[2]['text']='A letter predicts that the sister will vanish in a fire. Lin must respect her choice rather than decide her fate alone.'
        outline={'title':'Letters from Ten Years Ahead: A Family Divide','sections':sections,'demo_scenario':key,'demo_stage':2}
        return {'message':'[SCRIPTED RESPONSE] Loaded the prepared family-conflict revision.','updated':True,'outline':outline,'change_summary':'Scripted revision: family relationships affect the main conflict','demo':True}
    return {'message':'[SCRIPTED DEMO] No prepared continuation matches this request. The outline remains unchanged rather than pretending AI comprehension. Try a supported scenario or a working local model.','updated':False,'outline':None,'change_summary':'','demo':True}

def demo_evidence(payload):
    outline=payload.get('outline') or {}
    key=outline.get('demo_scenario')
    if key in ('memory','fantasy'):
        records=[dict(x,reviewed=False,selected=False) for x in SCENARIOS[key]['evidence']]
        if key=='fantasy':
            stage=int(outline.get('demo_stage',1))
            phrases={
               1:{'fantasy-priory':(2,'a betrayal by the royal family'), 'fantasy-hobbit':(0,'rescue a prince trapped in a mountain valley')},
               2:{'fantasy-priory':(2,'seize dragonfire to control mountain resources'), 'fantasy-hobbit':(0,'an ancient dragon has awakened')},
               3:{'fantasy-priory':(2,'The dragons fear another human betrayal'), 'fantasy-hobbit':(0,'The princess ventures into the Ashen Mountains to find the prince')},
            }
            for r in records:
                section,phrase=phrases.get(stage,{}).get(r['id'],(None,''))
                actual=(outline.get('sections') or [])
                if isinstance(section,int) and section < len(actual) and phrase in str(actual[section].get('text','')):
                    r['sectionIndex']=section;r['highlightText']=phrase
                else:
                    r['sectionIndex']=None;r['highlightText']=''
        elif key=='memory':
            for r in records:
                phrase='voluntarily sell a chosen personal memory'
                section=(outline.get('sections') or [])
                r['highlightText']=phrase if section and phrase in str(section[0].get('text','')) else ''
                r['sectionIndex']=0 if r['highlightText'] else None
        return {'records':records,'notice':'Manually curated publisher-linked book records (not live retrieval). Underlines and cards indicate thematic comparisons, not verified textual overlap, originality, or model inspiration sources.','demo':True}
    return {'records':[],'notice':'No candidate books are prepared for this offline scenario. An empty list does not establish originality.','demo':True}

def ollama_available(base=None):
    base=(base or os.getenv('OLLAMA_URL','http://127.0.0.1:11434')).rstrip('/')
    try:
        with urlopen(base+'/api/tags',timeout=3) as r:
            data=json.load(r)
            return [m.get('name') for m in data.get('models',[]) if isinstance(m,dict)]
    except (URLError,TimeoutError,OSError,ValueError):return []

def ollama_chat(payload, system, validate_outline):
    """Generate using a locally running Ollama model. No external service."""
    msg=str(payload.get('message','')).strip()
    if not msg or len(msg)>12000:raise ValueError('Enter a creative-writing message of 1–12,000 characters.')
    name=os.getenv('OLLAMA_MODEL','qwen2.5:3b')
    model_names=ollama_available()
    if name not in model_names:
        raise RuntimeError('Ollama model '+name+' was not found. Install Ollama and run: ollama pull '+name+'. Available local models: '+(', '.join(model_names) or 'none'))
    context={'current_outline':payload.get('currentOutline'), 'recent_conversation':(payload.get('history') or [])[-12:], 'author_selected_references':payload.get('selectedReferences') or [], 'new_message':msg}
    body={'model':name,'stream':False,'format':'json','messages':[{'role':'system','content':system},{'role':'user','content':json.dumps(context,ensure_ascii=False)}],'options':{'temperature':0.8}}
    url=os.getenv('OLLAMA_URL','http://127.0.0.1:11434').rstrip('/')+'/api/chat'
    try:
        req=Request(url,data=json.dumps(body,ensure_ascii=False).encode(),headers={'Content-Type':'application/json'},method='POST')
        with urlopen(req,timeout=160) as r:raw=json.load(r)
        obj=json.loads(raw['message']['content'])
        update=obj.get('update_outline') is True
        return {'message':str(obj.get('message','') or ('Outline updated.' if update else 'We can keep discussing.'))[:5000], 'updated':update,'outline':validate_outline(obj.get('outline')) if update else None,'change_summary':str(obj.get('change_summary',''))[:1000],'demo':False}
    except (HTTPError,URLError,KeyError,ValueError,TypeError,json.JSONDecodeError,TimeoutError) as e:
        raise RuntimeError('Ollama generation failed: '+str(e))
