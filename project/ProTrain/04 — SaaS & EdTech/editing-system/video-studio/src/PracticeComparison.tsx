import React from 'react';
import {AbsoluteFill, Audio, Interactive, Sequence, interpolate, staticFile, useCurrentFrame} from 'remotion';

const ink = '#172A35';
const teal = '#1B8E82';
const rise = (frame: number, delay = 0) => ({
  // The main thought is visible on the first frame; stagger only supporting elements.
  opacity: delay === 0 ? 1 : interpolate(frame, [delay, delay + 14], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
  transform: `translateY(${interpolate(frame, [delay, delay + 18], [32, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}px)`,
});

const Student = ({color}: {color: string}) => (
  <svg viewBox="0 0 200 180" width="200" height="180" aria-hidden="true">
    <circle cx="100" cy="52" r="32" fill={color}/>
    <path d="M35 166v-28c0-35 29-55 65-55s65 20 65 55v28" fill={color}/>
    <path d="m57 41 43-23 43 23-43 23Z" fill={ink}/>
    <path d="M143 42v36" stroke={ink} strokeWidth="6"/>
  </svg>
);

const Hook = () => {
  const f = useCurrentFrame();
  return <AbsoluteFill style={{alignItems:'center', justifyContent:'center', gap:38, padding:100}}>
    <Interactive.Div name="Opening question" style={{fontSize:102,fontWeight:700,...rise(f)}}>نفس المعدل؟</Interactive.Div>
    <div style={{display:'flex',gap:75,alignItems:'center',...rise(f,7)}}><Student color={teal}/><span style={{fontSize:90}}>=</span><Student color="#E9A56A"/></div>
    <Interactive.Div name="Opening payoff" style={{fontSize:58,lineHeight:1.6,textAlign:'center',...rise(f,18)}}>واش كيعني نفس<br/>الاختيارات الدراسية؟</Interactive.Div>
  </AbsoluteFill>;
};

const Profiles = () => {
  const f = useCurrentFrame();
  return <AbsoluteFill style={{padding:'350px 80px 260px',gap:55}}>
    <Interactive.Div name="Comparison title" style={{fontSize:68,fontWeight:700,textAlign:'center',...rise(f)}}>جوج ملفات مختلفين</Interactive.Div>
    <Interactive.Div name="Physical sciences profile" style={{background:'#fff',borderRadius:32,padding:'36px 45px',display:'flex',alignItems:'center',gap:28,...rise(f,5)}}>
      <Student color={teal}/><div><div style={{fontSize:50}}>علوم فيزيائية</div><bdi dir="ltr" style={{fontSize:70,fontWeight:700,color:teal}}>14.5 / 20</bdi></div>
    </Interactive.Div>
    <Interactive.Div name="Economics profile" style={{background:'#fff',borderRadius:32,padding:'36px 45px',display:'flex',alignItems:'center',gap:28,...rise(f,18)}}>
      <Student color="#E9A56A"/><div><div style={{fontSize:50}}>علوم اقتصادية</div><bdi dir="ltr" style={{fontSize:70,fontWeight:700,color:teal}}>14.5 / 20</bdi></div>
    </Interactive.Div>
    <Interactive.Div name="Comparison lesson" style={{fontSize:52,textAlign:'center',lineHeight:1.6,...rise(f,35)}}>المعدل متشابه،<br/>ولكن المسار الدراسي مختلف.</Interactive.Div>
  </AbsoluteFill>;
};

const Requirements = () => {
  const f = useCurrentFrame();
  return <AbsoluteFill style={{padding:'360px 100px 270px',gap:60}}>
    <Interactive.Div name="Requirements question" style={{fontSize:70,fontWeight:700,lineHeight:1.5,...rise(f)}}>شنو كيطلب<br/>هاد التكوين؟</Interactive.Div>
    <Interactive.Div name="Requirements document" style={{background:'#fff',borderRadius:28,padding:55,boxShadow:'0 18px 0 #d8e8e1',...rise(f,12)}}>
      <div style={{fontSize:50,color:teal,fontWeight:700,marginBottom:30}}>شروط التكوين</div>
      <div style={{fontSize:48,lineHeight:2}}>المسار الدراسي<br/>المواد المطلوبة<br/>الشروط المعلنة</div>
    </Interactive.Div>
    <Interactive.Div name="Mechanism" style={{fontSize:48,lineHeight:1.7,...rise(f,25)}}>كنقارنو معطيات الملف<br/>مع متطلبات كل تكوين.</Interactive.Div>
  </AbsoluteFill>;
};

const Lesson = () => {
  const f = useCurrentFrame();
  return <AbsoluteFill style={{background:ink,color:'#fff',padding:105,justifyContent:'center',gap:55}}>
    <Interactive.Div name="Final lesson" style={{fontSize:90,fontWeight:700,lineHeight:1.6,...rise(f)}}>المعدل بوحدو<br/><span style={{color:'#78D2BD'}}>ما كافيش.</span></Interactive.Div>
    <Interactive.Div name="Practical action" style={{fontSize:54,lineHeight:1.7,...rise(f,12)}}>قارن المسار الدراسي<br/>مع شروط التكوين.</Interactive.Div>
    <Interactive.Div name="Mixed-direction label" style={{fontSize:38,color:'#bed4d0',...rise(f,20)}}>قبل اختيارات <bdi dir="ltr">Campus France</bdi></Interactive.Div>
  </AbsoluteFill>;
};

export const PracticeComparison = () => <AbsoluteFill dir="rtl" lang="ar" style={{background:'#F8F5EE',color:ink,fontFamily:'Arial, sans-serif'}}>
  <Audio src={staticFile('practice/comparison-sound.wav')}/>
  <Sequence from={0} durationInFrames={90} name="01 Question"><Hook/></Sequence>
  <Sequence from={90} durationInFrames={180} name="02 Compare profiles"><Profiles/></Sequence>
  <Sequence from={270} durationInFrames={150} name="03 Requirements"><Requirements/></Sequence>
  <Sequence from={420} durationInFrames={120} name="04 Lesson"><Lesson/></Sequence>
  <Interactive.Div name="Practice disclosure" style={{position:'absolute',top:160,right:80,left:80,fontSize:30,textAlign:'center',background:'#e3eee8',color:ink,borderRadius:40,padding:16}}>مثال توضيحي — تدريب على المونتاج</Interactive.Div>
  <div style={{position:'absolute',bottom:220,right:80,left:80,height:5,background:'#9bb1aa'}}><Progress/></div>
</AbsoluteFill>;

const Progress = () => {
  const f = useCurrentFrame();
  return <div style={{height:'100%',width:`${(f+1)/540*100}%`,background:teal}}/>;
};
