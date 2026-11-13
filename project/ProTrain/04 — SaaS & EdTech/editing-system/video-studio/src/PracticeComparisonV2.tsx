import React from 'react';
import {AbsoluteFill, Easing, Interactive, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {Audio} from '@remotion/media';

const ink = '#172A35';
const paper = '#F8F5EE';
const teal = '#147F73';
const coral = '#B76539';
const ease = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.bezier(.16, 1, .3, 1)} as const;

const Scholar = ({color}: {color: string}) => <svg viewBox="0 0 160 160" width="100%" height="100%" aria-hidden="true">
  <circle cx="80" cy="80" r="78" fill={color} opacity=".12"/>
  <circle cx="80" cy="67" r="27" fill={color}/>
  <path d="M27 145v-16c0-30 23-47 53-47s53 17 53 47v16" fill={color}/>
  <path d="m31 45 49-24 49 24-49 25Z" fill={ink}/>
  <path d="M128 45v37" stroke={ink} strokeWidth="5"/>
</svg>;

const AnimatedProfileInner = ({color, label, side, style}: {color:string;label:string;side:'left'|'right';style?:React.CSSProperties}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const compact = interpolate(f, [7*fps, 8*fps], [0,1], ease);
  const compare = interpolate(f, [2.5*fps, 3.15*fps], [0,1], ease);
  return <div style={{position:'absolute',[side]:90,top:interpolate(f,[0,2.5*fps,3.15*fps,7*fps,8*fps],[630,630,565,565,495],ease),width:420,
    height:450+compare*165-compact*430,borderRadius:36,background:'#fff',border:`3px solid ${color}33`,boxShadow:`0 13px 0 ${color}16`,...style}}>
    <div style={{position:'absolute',top:42-compact*12,left:136-compact*108,width:148-compact*80,height:148-compact*80}}><Scholar color={color}/></div>
    <div style={{position:'absolute',top:225-compact*196,left:compact*122,width:420-compact*140,textAlign:'center',color,fontWeight:700,whiteSpace:'nowrap'}}>
      <bdi dir="ltr"><span style={{fontSize:128-compact*63}}>14.5</span><span style={{fontSize:36-compact*10}}> / 20</span></bdi>
    </div>
    <div dir="rtl" style={{position:'absolute',left:28+compact*80,right:28,top:410-compact*296,fontSize:52-compact*9,lineHeight:1.5,textAlign:'center',color:ink,
      opacity:interpolate(f,[2.5*fps+.2*fps,3.3*fps],[0,1],ease)}}>{label}</div>
    <svg width="104" height="68" viewBox="0 0 104 68" style={{position:'absolute',bottom:36,left:158,opacity:compare*(1-compact)}} aria-hidden="true">
      {side==='right' ? <g fill="none" stroke={color} strokeWidth="4"><ellipse cx="52" cy="34" rx="42" ry="16"/><ellipse cx="52" cy="34" rx="42" ry="16" transform="rotate(60 52 34)"/><ellipse cx="52" cy="34" rx="42" ry="16" transform="rotate(120 52 34)"/><circle cx="52" cy="34" r="5" fill={color}/></g>:
        <g fill={color}><rect x="12" y="35" width="16" height="30" rx="4"/><rect x="44" y="20" width="16" height="45" rx="4"/><rect x="76" y="3" width="16" height="62" rx="4"/></g>}
    </svg>
  </div>;
};

const AnimatedProfile = Interactive.create({Component:AnimatedProfileInner,layout:'none',schema:{
  color:{type:'color',default:teal},label:{type:'string',default:''},side:{type:'enum',variants:{left:{},right:{}},default:'right'},
}});

const Opening = () => <>
  <Interactive.Div name="Opening complete question part 1" style={{position:'absolute',top:305,left:90,right:90,fontSize:110,lineHeight:1.4,textAlign:'center',fontWeight:700}}>نفس المعدل…</Interactive.Div>
  <Interactive.Div name="Opening complete question part 2" style={{position:'absolute',top:1210,left:90,right:90,fontSize:101,lineHeight:1.5,textAlign:'center',fontWeight:700}}>نفس الاختيارات؟</Interactive.Div>
</>;

const Comparison = () => <>
  <Interactive.Div name="Different tracks title" style={{position:'absolute',top:290,left:90,right:90,fontSize:88,lineHeight:1.5,textAlign:'center',fontWeight:700}}>ولكن المسار مختلف</Interactive.Div>
  <Interactive.Div name="Equal score label" style={{position:'absolute',top:1285,left:90,right:90,fontSize:58,lineHeight:1.6,textAlign:'center'}}>نفس النقط، شُعب مختلفة.</Interactive.Div>
</>;

const ConnectingPaths = () => {
  const f=useCurrentFrame();
  const {fps}=useVideoConfig();
  return <svg viewBox="0 0 1080 1920" style={{position:'absolute',inset:0,width:'100%',height:'100%'}} aria-hidden="true">
    <path d="M780 680V785Q780 820 745 820H650Q610 820 610 860V908" pathLength="1" fill="none" stroke={teal} strokeWidth="9" strokeLinecap="round" strokeDasharray="1" strokeDashoffset={interpolate(f,[.55*fps,1.6*fps],[1,0],ease)}/>
    <path d="M300 680V785Q300 820 335 820H430Q470 820 470 860V908" pathLength="1" fill="none" stroke={coral} strokeWidth="9" strokeLinecap="round" strokeDasharray="1" strokeDashoffset={interpolate(f,[.8*fps,1.85*fps],[1,0],ease)}/>
    <circle cx="610" cy="916" r="10" fill={teal} opacity={interpolate(f,[1.45*fps,1.7*fps],[0,1],ease)}/>
    <circle cx="470" cy="916" r="10" fill={coral} opacity={interpolate(f,[1.7*fps,1.95*fps],[0,1],ease)}/>
  </svg>;
};

const RequirementRow = ({label, order}: {label:string;order:number}) => {
  const f=useCurrentFrame();
  const {fps}=useVideoConfig();
  const start=(1.7+order*.95)*fps;
  const highlight=interpolate(f,[start,start+.3*fps,start+.7*fps,start+1.05*fps],[0,1,1,.35],ease);
  return <div style={{position:'absolute',top:130+order*115,right:36,left:36,height:100,padding:'15px 28px',borderRadius:18,
    background:`rgba(20,127,115,${highlight*.1})`,borderRight:`7px solid rgba(20,127,115,${highlight})`,fontSize:53,lineHeight:'70px',fontWeight:700}}>{label}</div>;
};

const Requirements = () => <>
  <Interactive.Div name="Compare file with requirements" style={{position:'absolute',top:275,left:90,right:90,fontSize:88,lineHeight:1.5,textAlign:'center',fontWeight:700}}>قارن الملف بالشروط</Interactive.Div>
  <ConnectingPaths/>
  <Interactive.Div name="Illustrated requirements sheet" style={{position:'absolute',top:930,left:90,right:90,height:535,borderRadius:32,background:'#fff',boxShadow:'0 15px 0 #DFEAE3'}}>
    <div style={{position:'absolute',top:35,right:64,left:64,fontSize:56,color:teal,fontWeight:700}}>متطلبات التكوين</div>
    <RequirementRow label="الشعبة والمسار" order={0}/>
    <RequirementRow label="المواد المطلوبة" order={1}/>
    <RequirementRow label="الشروط المعلنة" order={2}/>
  </Interactive.Div>
  <Interactive.Div name="One file at a time" style={{position:'absolute',top:1525,left:90,right:90,fontSize:52,lineHeight:1.6,textAlign:'center'}}>كل ملف خاصّو يتراجع بوحدو.</Interactive.Div>
</>;

const FinalAction = () => <AbsoluteFill style={{background:ink,color:'#fff'}}>
  <Interactive.Div name="Decision context" style={{position:'absolute',top:310,left:90,right:90,fontSize:52,lineHeight:1.6,color:'#D5E8E1'}}>قبل ما تحسم اختياراتك</Interactive.Div>
  <Interactive.Div name="Final conclusion first line" style={{position:'absolute',top:490,left:90,right:90,fontSize:118,lineHeight:1.5,fontWeight:700}}>المعدل بوحدو</Interactive.Div>
  <Interactive.Div name="Final conclusion emphasis" style={{position:'absolute',top:675,left:90,right:90,fontSize:145,lineHeight:1.5,fontWeight:700,color:'#82DFC2'}}>ما كافيش.</Interactive.Div>
  <Interactive.Div name="Concrete review action" style={{position:'absolute',top:1090,left:90,right:90,padding:'50px 44px',borderRadius:32,background:'#E3F3EB',color:ink,fontSize:65,lineHeight:1.8,fontWeight:700,textAlign:'center'}}>راجع شروط التكوين<br/>وقارنها بملفك.</Interactive.Div>
  <Interactive.Div name="Programme context" style={{position:'absolute',top:1490,left:90,right:90,fontSize:48,lineHeight:1.7,color:'#D5E8E1'}}>باش تفهم اختيارك قبل الترشيح.</Interactive.Div>
</AbsoluteFill>;

const ChapterMarkers = () => {
  const f=useCurrentFrame();
  const stages=[0,75,225,405];
  return <div style={{position:'absolute',top:1740,right:90,left:90,display:'flex',gap:14}}>{stages.map((start,i)=><div key={start} style={{height:8,flex:1,borderRadius:8,background:f>=start?(f>=405?'#82DFC2':teal):'#C8D3CC',opacity:f>=start?1:.5}}/>)}</div>;
};

export const PracticeComparisonV2 = () => {
  const {fps}=useVideoConfig();
  return <AbsoluteFill dir="rtl" lang="ar" style={{background:paper,color:ink,fontFamily:'Tahoma, Arial, sans-serif',fontWeight:400}}>
    <Audio src={staticFile('practice/comparison-v2-sound.wav')}/>
    <Sequence from={0} durationInFrames={13.5*fps} name="Profiles persist from question into comparison">
      <AnimatedProfile name="Student A physical sciences" side="right" color={teal} label="علوم فيزيائية"/>
      <AnimatedProfile name="Student B economics" side="left" color={coral} label="علوم اقتصادية"/>
    </Sequence>
    <Sequence from={0} durationInFrames={2.5*fps} name="01 Same average question"><Opening/></Sequence>
    <Sequence from={2.5*fps} durationInFrames={5*fps} name="02 Different academic paths"><Comparison/></Sequence>
    <Sequence from={7.5*fps} durationInFrames={6*fps} name="03 Compare published requirements"><Requirements/></Sequence>
    <Sequence from={13.5*fps} durationInFrames={4.5*fps} name="04 Review before choosing"><FinalAction/></Sequence>
    <Interactive.Div name="Persistent synthetic disclosure" style={{position:'absolute',top:132,left:90,right:90,fontSize:29,textAlign:'center',borderRadius:40,padding:'15px 20px',background:'#E4EEE8',color:ink}}>تمرين بصري · مثال توضيحي</Interactive.Div>
    <ChapterMarkers/>
  </AbsoluteFill>;
};
