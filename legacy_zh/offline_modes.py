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
   'label':'记忆交易城市 · 来源审阅演示',
   'trigger':['记忆','memory','失忆'],
   'title':'记忆交易城的失落账本',
   'sections':[
    {'heading':'核心设定','text':'一座沿海城市允许成年人出售一段自愿选择的个人记忆，但无法出售别人对同一事件的记忆。每笔交易都有存档。'},
    {'heading':'人物与目标','text':'档案员玛拉发现父亲出卖了关于自己童年的记忆。她想知道那段记忆为何值得如此高价，以及父亲究竟想保护谁。'},
    {'heading':'冲突','text':'玛拉发现一批交易登记被修改。家人对同一事件的回忆出现矛盾，而经营交易所的机构拒绝公开原始记录。'},
    {'heading':'转折','text':'玛拉得知那些记忆不是简单消失，而被收购者用于重建一场被掩盖的集体事故。她必须决定公开真相还是保护仍活着的家人。'},
    {'heading':'结局方向','text':'她选择公开账本的造假方式，但不擅自揭露出售者的私人记忆。城市开始重新讨论记忆买卖的边界。'}],
   'evidence':[{'id':'memory-1','title':'The Memory Police — Yoko Ogawa','url':MEMORY_URL,'sectionIndex':0,'comparison':'人工准备的主题层面对照：这部小说涉及记忆消失及社会关系；示例故事则涉及自愿出售记忆。仅依据出版社作品信息，不表示模型参考过该书。','kind':'potentially_similar'}]
 },
 'mystery': {
   'label':'十年后的来信 · 多轮创作演示',
   'trigger':['邮递员','来信','十年后','letter','postman'],
   'title':'十年后的邮戳',
   'sections':[
    {'heading':'故事起点','text':'小镇邮递员林舟接到一封寄件日期为十年后的信，信中准确写出第二天发生的小事。'},
    {'heading':'主人公','text':'林舟原本只想按部就班工作，却因为另一封预告火灾的信开始调查寄件人。'},
    {'heading':'主要冲突','text':'有人利用未来信件操纵镇民抉择，林舟不得不判断改变未来是否会伤害另一个家庭。'},
    {'heading':'发展与转折','text':'林舟发现信件来自不同可能的未来，并非一个确定的命运；每次干预都让下一封信出现不同版本。'},
    {'heading':'可能结局','text':'林舟公开信件的规律，让镇民共同作决定，不再让一个匿名寄件人控制每个人的命运。'}],
   'evidence':[]
 },
 'fantasy': {
   'label':'奇幻救援 · 新元素融合演示',
   'trigger':['公主','王子','dragon','龙','奇幻'],
   'title':'穿越灰烬山脉的救援',
   'sections':[
    {'heading':'故事起点','text':'一位力大无穷却不愿继承王位的公主决定救出被困山谷的王子，并证明救援不必依靠王国的旧预言。'},
    {'heading':'角色关系','text':'王子掌握古地图知识，但不擅长战斗；公主精于行动，却不懂山区居民与王室之间的旧约。两人必须互相信任。'},
    {'heading':'冲突','text':'救援途中，王国军队企图封锁山路，因为他们害怕山谷中有人知道王室曾经的背叛。'},
    {'heading':'转折','text':'公主发现所谓囚禁其实是一场政治交易，王子选择留下是为了保护山谷村民。'},
    {'heading':'结局方向','text':'两人公开旧约，拒绝利用传统婚约解决政治冲突，转而推动双方重新谈判。'}],
   'evidence':[
    {'id':'fantasy-priory','title':'The Priory of the Orange Tree — Samantha Shannon','url':PRIORY_URL,'sectionIndex':2,'comparison':'人工预选的主题对照：该书涉及龙、王权和政治权力；V1关联的是王室背叛这一宽泛政治冲突，V2–V3才涉及龙族。仅说明主题交集，不表示相同情节、文字重复或创作来源。','kind':'manually_curated','source':'Bloomsbury Publishing · publisher book page','review_basis':'出版社作品介绍（人工核对）'},
    {'id':'fantasy-hobbit','title':'The Hobbit — J. R. R. Tolkien','url':HOBBIT_URL,'sectionIndex':3,'comparison':'人工预选的宽泛题材对照（相关性较弱）：该书包含冒险与龙的元素；V1仅关联营救与冒险这一一般母题，并非指具体桥段重合；V2–V3才引入龙。不能据此认定文本或情节相似。','kind':'manually_curated','source':'HarperCollins / HarperReach · official product page','review_basis':'出版方产品介绍（人工核对）'}]
 }
}

def scenario_for(message,current=None):
    if current and current.get('demo_scenario') in SCENARIOS: return current['demo_scenario']
    text=message.lower()
    for name,s in SCENARIOS.items():
        if any(w in text for w in s['trigger']):return name
    return None

def mock_chat(payload):
    """Only fixed, visible demo scripts. Arbitrary text never pretends to be generated."""
    message=str(payload.get('message','')).strip()
    if not message: raise ValueError('请输入消息。')
    previous=payload.get('currentOutline')
    context=previous if isinstance(previous,dict) else None
    key=scenario_for(message,context)
    if not key:
        return {'message':'【离线脚本演示】当前输入不属于预设场景，无法智能创作。请选择一个演示案例，或切换到Ollama/OpenAI模式。','updated':False,'outline':None,'change_summary':'','demo':True}
    script=SCENARIOS[key]
    if context is None:
        outline={'title':script['title'],'sections':[dict(x) for x in script['sections']],'demo_scenario':key,'demo_stage':1}
        return {'message':'【模拟响应】已加载“'+script['label']+'”的第一版示例大纲。此处没有调用AI。','updated':True,'outline':outline,'change_summary':'加载预编写演示场景','demo':True}
    stage=int(context.get('demo_stage',1))
    low=message.lower()
    if any(w in low for w in ['讨论','解释','为什么','先聊','不更新','不要更新','建议','想法呢','?','？']):
        return {'message':'【模拟响应】我可以说明演示操作，但离线脚本不能像真实模型一样理解这条自由问题。大纲未发生变化。','updated':False,'outline':None,'change_summary':'','demo':True}
    if key=='fantasy' and ('龙' in low or 'dragon' in low) and stage==1:
        outline={'title':'灰烬山脉与最后一条龙','sections':[
          {'heading':'故事起点','text':'强壮的公主出发营救山谷中的王子，途中发现沉睡的古龙已经苏醒，封锁山路的并非普通军队而是猎龙团。'},
          {'heading':'人物与关系','text':'王子能解读龙语，公主负责保护队伍；一条幼龙误认公主为曾经救过它的人，成为不可靠却关键的伙伴。'},
          {'heading':'冲突升级','text':'王国试图夺取龙焰控制山区资源。公主必须在迅速救出王子和帮助龙族摆脱追捕之间选择。'},
          {'heading':'主要转折','text':'王子留下不是因为无力逃走，而是在守护一处龙卵遗址。公主发现这场营救牵涉王国与龙族长期被掩盖的契约。'},
          {'heading':'结局方向','text':'公主、王子与龙族一同揭露谎言，阻止全面战争，救援从个人行动变为改变政治关系的冒险。'}], 'demo_scenario':key,'demo_stage':2}
        return {'message':'【模拟响应】已切换到预写的“加入龙”第二幕示例，龙影响了整个主要冲突。这只是固定脚本，不代表能够理解任意新要求。','updated':True,'outline':outline,'change_summary':'脚本示范：龙改变了救援动机、人物关系与冲突','demo':True}
    # Third fixed scene: specifically supported author request about prince/dragon relationships.
    # This is NOT semantic AI understanding; it is a pre-authored revision of the full outline.
    if key=='fantasy' and stage==2 and (('王子' in low and '龙' in low) or ('人物' in low and '关系' in low) or ('角色' in low and '关系' in low)):
        outline={'title':'灰烬山脉：王子与龙族的秘密盟约','sections':[
          {'heading':'故事起点','text':'公主深入灰烬山脉寻找王子，却发现王子主动留下来照料一条受伤的幼龙。公主从营救者转为必须理解双方立场的谈判者。'},
          {'heading':'人物与关系','text':'王子曾秘密向龙族长老承诺保护龙卵遗址；幼龙把他当作可信任的监护人，而公主起初认为这份承诺让王子背弃王国。三方从误解、争执走向相互信任。'},
          {'heading':'冲突升级','text':'猎龙团以王子的承诺为叛国证据，试图逼公主交出王子。龙族担心人类再次背约，要求王子留下作担保。'},
          {'heading':'主要转折','text':'公主发现当年的王室契约其实由父辈撕毁；王子并非被动受困，而是以自己的自由换取龙族暂缓报复。公主决定将私人救援升级为公开谈判。'},
          {'heading':'结局方向','text':'公主公开旧约与双方隐瞒的事实，王子向龙族说明自己承诺的边界，龙族长老同意共同监督新的停战条约。三人的关系由保护与被保护转为共同承担责任。'}], 'demo_scenario':key,'demo_stage':3}
        return {'message':'【模拟响应】已加载预写的第三轮“王子与龙族关系”版本；人物关系改变了营救动机、政治冲突和结局。这不是自由AI理解。右侧可继续审阅人工核实的主题候选作品。','updated':True,'outline':outline,'change_summary':'固定脚本第三轮：强化王子—幼龙—公主关系及其情节后果','demo':True}
    if key=='mystery' and ('妹妹' in low or '姐姐' in low or '家人' in low) and stage==1:
        sections=[dict(x) for x in context['sections']]
        sections[1]['text']='林舟与疏远的妹妹共同调查未来信件，妹妹曾因他错过一封紧急通知而不再信任他。'
        sections[2]['text']='信件预示妹妹会在大火中失踪，林舟必须相信她自己的选择，而非单方面替她决定命运。'
        outline={'title':'十年后的邮戳：家人的分歧','sections':sections,'demo_scenario':key,'demo_stage':2}
        return {'message':'【模拟响应】已加载预写的家人冲突第二版。','updated':True,'outline':outline,'change_summary':'脚本示范：增加家庭关系对主线的影响','demo':True}
    return {'message':'【离线脚本演示】该场景没有匹配这一指令的后续预写版本。为避免假装AI理解，本轮不会重写大纲；你可以使用已支持的案例或切换真实本地模型。','updated':False,'outline':None,'change_summary':'','demo':True}

def demo_evidence(payload):
    outline=payload.get('outline') or {}
    key=outline.get('demo_scenario')
    if key in ('memory','fantasy'):
        records=[dict(x,reviewed=False,selected=False) for x in SCENARIOS[key]['evidence']]
        # Only match actual phrases present in the outline; no fabricated link to whole paragraphs.
        # The annotations are thematic comparison prompts, NOT confirmed textual matches.
        if key=='fantasy':
            stage=int(outline.get('demo_stage',1))
            phrases={
               1:{'fantasy-priory':(2,'王室曾经的背叛'), 'fantasy-hobbit':(0,'救出被困山谷的王子')},  # V1: broad political-intrigue/adventure comparisons only; no dragon-specific claim
               2:{'fantasy-priory':(2,'王国试图夺取龙焰控制山区资源'), 'fantasy-hobbit':(0,'沉睡的古龙已经苏醒')},
               3:{'fantasy-priory':(2,'龙族担心人类再次背约'), 'fantasy-hobbit':(0,'公主深入灰烬山脉寻找王子')},
            }
            for r in records:
                section,phrase=phrases.get(stage,{}).get(r['id'],(None,''))
                actual=(outline.get('sections') or [])
                if isinstance(section,int) and section < len(actual) and phrase in str(actual[section].get('text','')):
                    r['sectionIndex']=section
                    r['highlightText']=phrase
                else:
                    r['sectionIndex']=None
                    r['highlightText']=''
        elif key=='memory':
            for r in records:
                phrase='出售一段自愿选择的个人记忆'
                section=(outline.get('sections') or [])
                r['highlightText']=phrase if section and phrase in str(section[0].get('text','')) else ''
                r['sectionIndex']=0 if r['highlightText'] else None
        return {'records':records, 'notice':'人工预选且核对书目信息的真实作品链接（非实时检索）。下划线与卡片标示主题对照，不代表确认的文本重复、原创性判断或模型的真实灵感来源。','demo':True}
    return {'records':[], 'notice':'离线模式未对本场景准备候选作品。无候选结果不代表内容原创。','demo':True}

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
    if not msg or len(msg)>12000:raise ValueError('请输入 1–12000 字的创作消息。')
    name=os.getenv('OLLAMA_MODEL','qwen2.5:3b')
    model_names=ollama_available()
    if name not in model_names:
        raise RuntimeError('未找到Ollama模型 '+name+'。请先安装Ollama并运行 ollama pull '+name+'。本地可用模型：'+(', '.join(model_names) or '无'))
    context={'current_outline':payload.get('currentOutline'), 'recent_conversation':(payload.get('history') or [])[-12:], 'author_selected_references':payload.get('selectedReferences') or [], 'new_message':msg}
    body={'model':name,'stream':False,'format':'json','messages':[{'role':'system','content':system},{'role':'user','content':json.dumps(context,ensure_ascii=False)}],'options':{'temperature':0.8}}
    url=os.getenv('OLLAMA_URL','http://127.0.0.1:11434').rstrip('/')+'/api/chat'
    try:
        req=Request(url,data=json.dumps(body,ensure_ascii=False).encode(),headers={'Content-Type':'application/json'},method='POST')
        with urlopen(req,timeout=160) as r:raw=json.load(r)
        obj=json.loads(raw['message']['content'])
        update=obj.get('update_outline') is True
        return {'message':str(obj.get('message','') or ('已更新大纲' if update else '我们可以继续讨论。'))[:5000], 'updated':update,'outline':validate_outline(obj.get('outline')) if update else None,'change_summary':str(obj.get('change_summary',''))[:1000],'demo':False}
    except (HTTPError,URLError,KeyError,ValueError,TypeError,json.JSONDecodeError,TimeoutError) as e:
        raise RuntimeError('Ollama生成失败：'+str(e))
