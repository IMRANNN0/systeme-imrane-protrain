import React, {useEffect, useState} from 'react';
import type {Caption} from '@remotion/captions';
import {Audio} from '@remotion/media';
import {AbsoluteFill, Img, Interactive, Sequence, cancelRender, continueRender, delayRender, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';

type Scene = {id: string; startSeconds: number; endSeconds: number};
type Plan = {width: number; height: number; fps: number; durationInFrames: number; scenes: Scene[]; captions: Caption[]};
let planPromise: Promise<Plan> | undefined;
let fontPromise: Promise<FontFace> | undefined;

export const loadPilot001Plan = () => {
  if (!planPromise) planPromise = fetch(staticFile('pilot-001/edit-plan.json')).then(response => {
    if (!response.ok) throw new Error('Pilot001 edit plan could not be loaded');
    return response.json();
  }).then((plan: Plan) => {
    if (!Number.isInteger(plan.durationInFrames) || plan.durationInFrames <= 0 || plan.scenes.length !== 7 || !Array.isArray(plan.captions)) throw new Error('Invalid Pilot001 edit plan');
    let end = 0;
    plan.scenes.forEach((scene, index) => {
      if (scene.id !== `S0${index + 1}` || Math.abs(scene.startSeconds - end) > 0.0001 || scene.endSeconds <= scene.startSeconds) throw new Error('Pilot001 scenes must be ordered, adjacent and nonempty');
      end = scene.endSeconds;
    });
    if (Math.round(end * plan.fps) !== plan.durationInFrames) throw new Error('Pilot001 plan end does not match duration');
    return plan;
  });
  return planPromise;
};

const ExplanationLabel = () => <Interactive.Div name="Persistent explanatory label" style={{position:'absolute',top:250,right:140,padding:'8px 24px',fontSize:35,fontWeight:700,color:'#0F2A1F',backgroundColor:'#F2A541',borderRadius:6}}>شرح توضيحي</Interactive.Div>;

const Folder = () => <Img name="Illustrative physical folder photograph, not a real report" src={staticFile('pilot-001/explanatory-folder-v1.png')} style={{position:'absolute',width:1080,height:1920,objectFit:'cover'}}/>;

const Hook = () => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  return <AbsoluteFill>
    <Img name="Fictional adult student context photograph" src={staticFile('pilot-001/context-student-v1.png')} style={{position:'absolute',width:1080,height:1920,objectFit:'cover',scale:interpolate(frame,[0,durationInFrames],[1,1.025],{extrapolateLeft:'clamp',extrapolateRight:'clamp'}),transformOrigin:'50% 50%'}}/>
    <Interactive.Div name="Campus France context" dir="ltr" style={{position:'absolute',top:265,left:100,right:140,fontSize:62,fontWeight:750,color:'#0F2A1F',backgroundColor:'#F6F4EE',padding:'10px 24px',textAlign:'center'}}>Campus France</Interactive.Div>
    <Interactive.Div name="Formation choice question" style={{position:'absolute',top:390,left:100,right:140,fontSize:77,lineHeight:1.5,fontWeight:850,color:'#F6F4EE',backgroundColor:'#0A6B43',padding:'8px 22px 20px',textAlign:'center'}}>محتار شنو تختار؟</Interactive.Div>
  </AbsoluteFill>;
};

const ProfileConditions = () => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  return <AbsoluteFill style={{backgroundColor:'#F6F4EE'}}>
    <ExplanationLabel/>
    <Interactive.Div name="University name is one part" style={{position:'absolute',top:370,left:100,right:140,fontSize:64,lineHeight:1.5,fontWeight:800,color:'#0F2A1F',textAlign:'right'}}>ماشي غير اسم الجامعة</Interactive.Div>
    <Interactive.Div name="Academic profile information" style={{position:'absolute',top:570,left:140,right:180,padding:'35px 35px',fontSize:70,fontWeight:800,lineHeight:1.5,color:'#F6F4EE',backgroundColor:'#0A6B43',borderRadius:12,translate:interpolate(frame,[0,15],['0px 25px','0px 0px'],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}}>الملف الدراسي ديالك</Interactive.Div>
    <Interactive.Div name="Comparison connection" dir="ltr" style={{position:'absolute',top:755,left:420,width:200,textAlign:'center',fontSize:76,color:'#0A6B43',opacity:interpolate(frame,[durationInFrames*0.27,durationInFrames*0.33],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}}>↕</Interactive.Div>
    <Interactive.Div name="Published formation requirements" style={{position:'absolute',top:875,left:140,right:180,padding:'30px 35px',fontSize:69,fontWeight:800,lineHeight:1.5,color:'#0F2A1F',backgroundColor:'#F2A541',borderRadius:12,opacity:interpolate(frame,[durationInFrames*0.27,durationInFrames*0.33],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}}>شروط التكوين</Interactive.Div>
  </AbsoluteFill>;
};

const AuthenticForm = () => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  return <AbsoluteFill style={{backgroundColor:'#F6F4EE'}}>
    <Interactive.Div name="Real form title" style={{position:'absolute',top:285,left:100,right:140,fontSize:68,lineHeight:1.35,fontWeight:850,color:'#0F2A1F',textAlign:'right'}}>كتعمّر معلوماتك الدراسية</Interactive.Div>
    <Interactive.Div name="Free profile label" style={{position:'absolute',top:505,right:140,padding:'8px 30px',fontSize:50,lineHeight:1.4,fontWeight:800,color:'#F6F4EE',backgroundColor:'#0A6B43',borderRadius:8}}>مجاناً</Interactive.Div>
    <Interactive.Div name="Authentic public form camera viewport" style={{position:'absolute',top:635,left:90,width:880,height:410,overflow:'hidden',borderRadius:12,border:'2px solid #0A6B43',backgroundColor:'#FFFFFF'}}>
      <Img name="Unaltered authentic form screenshot; camera crop only" src={staticFile('pilot-001/landing-form-original.jpg')} style={{position:'absolute',width:2530,height:1424,left:-590,top:-800,objectFit:'contain',scale:interpolate(frame,[0,durationInFrames],[1,1.025],{extrapolateLeft:'clamp',extrapolateRight:'clamp'}),transformOrigin:'50% 50%'}}/>
    </Interactive.Div>
  </AbsoluteFill>;
};

const Proposals = () => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  return <AbsoluteFill>
    <Folder/><ExplanationLabel/>
    <Interactive.Div name="Personalized report offer" style={{position:'absolute',top:365,left:100,right:140,padding:'14px 30px',fontSize:76,lineHeight:1.5,fontWeight:850,color:'#0F2A1F',backgroundColor:'#F6F4EE',textAlign:'right'}}>تقرير مخصص حسب ملفك</Interactive.Div>
    <Interactive.Div name="Up to seven, not guaranteed seven" style={{position:'absolute',top:650,left:120,right:160,padding:'22px 32px',fontSize:82,lineHeight:1.45,fontWeight:850,color:'#F6F4EE',backgroundColor:'#0A6B43',borderRadius:8,translate:interpolate(frame,[0,durationInFrames*0.15],['0px 30px','0px 0px'],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}}>حتى لسبعة تكوينات مقترحة</Interactive.Div>
    <Interactive.Div name="Paid full report distinction" style={{position:'absolute',top:965,left:120,right:160,fontSize:48,fontWeight:700,color:'#0F2A1F',backgroundColor:'#F6F4EE',padding:'12px 20px',textAlign:'center'}}>التقرير الكامل عرض مدفوع</Interactive.Div>
  </AbsoluteFill>;
};

const ReasonsConditions = () => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  return <AbsoluteFill>
    <Folder/><ExplanationLabel/>
    <Interactive.Div name="Understand each proposal" style={{position:'absolute',top:370,left:100,right:140,padding:'14px 26px',fontSize:70,lineHeight:1.5,fontWeight:850,color:'#0F2A1F',backgroundColor:'#F6F4EE',textAlign:'right'}}>مع كل تكوين مقترح</Interactive.Div>
    <Interactive.Div name="Reason for recommendation" style={{position:'absolute',top:650,left:120,right:160,padding:'25px 32px',fontSize:75,lineHeight:1.5,fontWeight:850,color:'#F6F4EE',backgroundColor:'#0A6B43',borderRadius:8}}>علاش تقترحات ليك؟</Interactive.Div>
    <Interactive.Div name="Admission conditions reveal" style={{position:'absolute',top:875,left:120,right:160,padding:'24px 32px',fontSize:70,lineHeight:1.5,fontWeight:850,color:'#0F2A1F',backgroundColor:'#F2A541',borderRadius:8,opacity:interpolate(frame,[durationInFrames*0.5,durationInFrames*0.6],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'}),translate:interpolate(frame,[durationInFrames*0.5,durationInFrames*0.6],['0px 22px','0px 0px'],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}}>شنو شروط القبول؟</Interactive.Div>
  </AbsoluteFill>;
};

const Steps = () => <AbsoluteFill>
  <Folder/><ExplanationLabel/>
  <Interactive.Div name="Pre-application steps heading" style={{position:'absolute',top:400,left:100,right:140,padding:'18px 28px',fontSize:75,lineHeight:1.5,fontWeight:850,color:'#0F2A1F',backgroundColor:'#F6F4EE',textAlign:'right'}}>شنو خاصك تراجع؟</Interactive.Div>
  <Interactive.Div name="Review steps before applying, no submission claim" style={{position:'absolute',top:720,left:120,right:160,padding:'30px 32px',fontSize:78,lineHeight:1.6,fontWeight:850,color:'#F6F4EE',backgroundColor:'#0A6B43',borderRadius:8}}>الخطوات قبل الترشيح</Interactive.Div>
</AbsoluteFill>;

const Action = () => <AbsoluteFill style={{backgroundColor:'#0A6B43'}}>
  <Interactive.Div name="Free profile CTA" style={{position:'absolute',top:340,left:100,right:140,padding:'20px 30px',fontSize:90,lineHeight:1.5,fontWeight:850,color:'#0F2A1F',backgroundColor:'#F2A541',textAlign:'center'}}>عمّر ملفك مجاناً</Interactive.Div>
  <Interactive.Div name="Inspect full paid report offer" style={{position:'absolute',top:650,left:100,right:140,fontSize:70,lineHeight:1.6,fontWeight:800,color:'#F6F4EE',textAlign:'center'}}>شوف عرض التقرير الكامل</Interactive.Div>
  <Interactive.Div name="Purchase remains viewer decision" style={{position:'absolute',top:810,left:100,right:140,fontSize:57,lineHeight:1.6,fontWeight:600,color:'#F6F4EE',textAlign:'center'}}>قبل ما تقرر تشريه</Interactive.Div>
  <Interactive.Div name="Actual public landing destination" dir="ltr" style={{position:'absolute',top:945,left:100,right:140,fontFamily:'Arial, sans-serif',fontSize:34,lineHeight:1.4,fontWeight:600,color:'#F6F4EE',textAlign:'center'}}>protraincompany.com<br/>/en/etudier-en-france/campus-france</Interactive.Div>
</AbsoluteFill>;

const Captions = ({captions}: {captions: Caption[]}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const caption = captions.find(item => frame / fps * 1000 >= item.startMs && frame / fps * 1000 < item.endMs);
  if (!caption) return null;
  return <Interactive.Div name="Exact narration phrase captions from edit plan" dir="rtl" style={{position:'absolute',top:1075,left:100,right:140,padding:'14px 22px 18px',borderRadius:10,fontSize:48,lineHeight:1.45,fontWeight:700,color:'#F6F4EE',backgroundColor:'#0F2A1F',textAlign:'center',whiteSpace:'pre-wrap',unicodeBidi:'plaintext'}}>{caption.text}</Interactive.Div>;
};

export const Pilot001 = () => {
  const [plan, setPlan] = useState<Plan | null>(null);
  const [handle] = useState(() => delayRender('Pilot001 authoritative plan and Cairo font'));
  const {fps} = useVideoConfig();
  useEffect(() => {
    if (!fontPromise) fontPromise = new FontFace('Pilot Cairo', `url("${staticFile('pilot-001/cairo-arabic.woff2')}")`, {weight:'200 1000'}).load().then(font => { document.fonts.add(font); return font; });
    Promise.all([loadPilot001Plan(), fontPromise]).then(([loaded]) => { setPlan(loaded); continueRender(handle); }).catch(cancelRender);
  }, [handle]);
  if (!plan) return null;
  const start = (id: string) => Math.round(plan.scenes.find(scene => scene.id === id)!.startSeconds * fps);
  const length = (id: string) => Math.round(plan.scenes.find(scene => scene.id === id)!.endSeconds * fps) - start(id);
  return <AbsoluteFill dir="rtl" lang="ar-MA" style={{fontFamily:'Pilot Cairo, sans-serif',backgroundColor:'#F6F4EE',color:'#0F2A1F'}}>
    <Audio name="Approved generic Darija voice, no music" src={staticFile('pilot-001/voice-mix-v1.wav')}/>
    <Sequence name="S01 Formation-choice hook" from={start('S01')} durationInFrames={length('S01')}><Hook/></Sequence>
    <Sequence name="S02 Profile and conditions explanation" from={start('S02')} durationInFrames={length('S02')}><ProfileConditions/></Sequence>
    <Sequence name="S03 Authentic public form" from={start('S03')} durationInFrames={length('S03')}><AuthenticForm/></Sequence>
    <Sequence name="S04 Labelled report metaphor" from={start('S04')} durationInFrames={length('S04')}><Proposals/></Sequence>
    <Sequence name="S05 Reason then conditions" from={start('S05')} durationInFrames={length('S05')}><ReasonsConditions/></Sequence>
    <Sequence name="S06 Steps before applying" from={start('S06')} durationInFrames={length('S06')}><Steps/></Sequence>
    <Sequence name="S07 Free entry and full-report offer" from={start('S07')} durationInFrames={length('S07')}><Action/></Sequence>
    <Interactive.Div name="Original corporate logo surface" style={{position:'absolute',top:105,left:100,width:128,height:128,borderRadius:64,backgroundColor:'#F6F4EE',display:'flex',alignItems:'center',justifyContent:'center'}}><Img name="Original ProTrain corporate logo" src={staticFile('pilot-001/protrain-logo-site.png')} style={{width:110,height:110,objectFit:'contain'}}/></Interactive.Div>
    <Interactive.Div name="Plain Match product label" dir="ltr" style={{position:'absolute',top:135,right:140,fontSize:43,fontWeight:800,color:'#0F2A1F',backgroundColor:'#F6F4EE',padding:'6px 20px',borderRadius:6}}>ProTrain Match</Interactive.Div>
    <Captions captions={plan.captions}/>
  </AbsoluteFill>;
};
