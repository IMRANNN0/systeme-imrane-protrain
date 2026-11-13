import React from 'react';
import {AbsoluteFill, Audio, Easing, Img, Interactive, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';

const ink='#232A2C';
const clamp={extrapolateLeft:'clamp',extrapolateRight:'clamp'} as const;
const lift={...clamp,easing:Easing.bezier(.55,0,.15,1)};

const Papers = () => {
  const f=useCurrentFrame();
  const {fps}=useVideoConfig();
  return <>
    <Interactive.Div name="Science notebook" style={{position:'absolute',left:75,top:735,width:440,height:850,
      translate:interpolate(f,[2.05*fps,3.5*fps],['0px 0px','-10px -35px'],lift),
      rotate:interpolate(f,[2.05*fps,2.8*fps,3.5*fps],['-4deg','-7deg','-6deg'],clamp),filter:'drop-shadow(14px 22px 12px #4B433E2B)'}}>
      <Img src={staticFile('craft/science-paper.svg')} style={{width:440,height:850}}/>
      <Interactive.Div name="Physical science track" style={{position:'absolute',top:160,left:57,right:25,fontSize:64,fontWeight:700,lineHeight:1.7,textAlign:'center',color:'#37697B'}}>علوم<br/>فيزيائية</Interactive.Div>
    </Interactive.Div>
    <Interactive.Div name="Economics notebook" style={{position:'absolute',right:70,top:760,width:440,height:850,
      translate:interpolate(f,[2.18*fps,3.6*fps],['0px 0px','12px -35px'],lift),
      rotate:interpolate(f,[2.18*fps,2.9*fps,3.6*fps],['4deg','7.5deg','6deg'],clamp),filter:'drop-shadow(14px 22px 12px #4B433E2B)'}}>
      <Img src={staticFile('craft/economics-paper.svg')} style={{width:440,height:850}}/>
      <Interactive.Div name="Economics track" style={{position:'absolute',top:160,left:57,right:25,fontSize:64,fontWeight:700,lineHeight:1.7,textAlign:'center',color:'#AC552F'}}>علوم<br/>اقتصادية</Interactive.Div>
    </Interactive.Div>
  </>;
};

const GradeBand = () => {
  const f=useCurrentFrame();
  const {fps}=useVideoConfig();
  return <>
    <div style={{position:'absolute',left:90,top:1050,width:900,height:70,borderRadius:'50%',background:'#413727',filter:'blur(25px)',
      opacity:interpolate(f,[0,1.4*fps,1.6*fps,2.2*fps,3.6*fps],[.12,.12,.2,.12,0],clamp)}}/>
    <Interactive.Div name="Grade as an obstruction lifted away" style={{position:'absolute',left:75,top:535,width:930,height:640,zIndex:10,transformOrigin:'50% 0%',
      transform:`perspective(1800px) translateY(${interpolate(f,[0,2.2*fps,3.6*fps],[0,0,-1000],lift)}px) rotateX(${interpolate(f,[0,1.4*fps,1.6*fps,2.2*fps,3.6*fps],[0,0,-3,63,9],lift)}deg) rotateZ(${interpolate(f,[0,2.2*fps,3.25*fps,3.6*fps],[-2,-2,-10,-8],clamp)}deg)`,
      filter:`drop-shadow(14px ${interpolate(f,[1.4*fps,1.6*fps,2.2*fps],[12,25,50],clamp)}px ${interpolate(f,[1.4*fps,2.2*fps],[10,27],clamp)}px #57422E45)`}}>
      <Img src={staticFile('craft/grade-band.svg')} style={{width:930,height:640}}/>
      <div style={{position:'absolute',left:35,top:125,width:410,textAlign:'center',color:ink,fontFamily:'Georgia, serif',fontSize:175,fontWeight:700,rotate:'1.5deg'}}><bdi dir="ltr">14.5</bdi></div>
      <div style={{position:'absolute',right:25,top:137,width:410,textAlign:'center',color:ink,fontFamily:'Georgia, serif',fontSize:175,fontWeight:700,rotate:'-1deg'}}><bdi dir="ltr">14.5</bdi></div>
      <div dir="ltr" style={{position:'absolute',top:363,left:110,fontSize:41,color:'#4A3B29',fontFamily:'Georgia, serif'}}>/ 20</div>
      <div dir="ltr" style={{position:'absolute',top:375,right:110,fontSize:41,color:'#4A3B29',fontFamily:'Georgia, serif'}}>/ 20</div>
      <svg width="850" height="80" viewBox="0 0 850 80" style={{position:'absolute',left:35,top:430}} aria-hidden="true"><path d="M22 42Q181 22 391 40M470 43Q652 25 825 46" fill="none" stroke="#453626" strokeWidth="7" strokeLinecap="round" opacity=".65"/></svg>
    </Interactive.Div>
  </>;
};

export const CraftStudy = () => {
  const {fps}=useVideoConfig();
  return <AbsoluteFill dir="rtl" lang="ar" style={{color:ink,fontFamily:'Tahoma, Arial, sans-serif'}}>
    <Img src={staticFile('craft/desk.svg')} style={{position:'absolute',width:1080,height:1920}}/>
    <Audio src={staticFile('craft/paper-action.wav')}/>
    <Papers/>
    <Sequence from={0} durationInFrames={2.2*fps} name="The grade dominates before the lift">
      <Interactive.Div name="Same average setup" style={{position:'absolute',top:295,right:95,left:95,fontSize:96,lineHeight:1.55,fontWeight:700,textAlign:'center'}}>نفس المعدّل…</Interactive.Div>
    </Sequence>
    <Sequence from={3.6*fps} durationInFrames={1.2*fps} name="Different trajectories revealed">
      <Interactive.Div name="Different academic path" style={{position:'absolute',top:330,right:95,left:95,fontSize:85,lineHeight:1.6,fontWeight:700,textAlign:'center'}}>ولكن المسار مختلف.</Interactive.Div>
    </Sequence>
    <Sequence from={4.8*fps} durationInFrames={4.2*fps} name="Practical conclusion in the same scene">
      <Interactive.Div name="Conclusion first line" style={{position:'absolute',top:280,right:95,left:95,fontSize:92,fontWeight:700,lineHeight:1.5}}>المعدّل بوحدو</Interactive.Div>
      <Interactive.Div name="Conclusion emphasis" style={{position:'absolute',top:440,right:95,left:95,fontSize:132,fontWeight:700,lineHeight:1.5}}>ما كافيش.</Interactive.Div>
      <Interactive.Div name="Review published requirements" style={{position:'absolute',top:1660,right:160,left:95,fontSize:52,lineHeight:1.6,fontWeight:700,textAlign:'center'}}>قارن ملفك<br/>بشروط التكوين.</Interactive.Div>
    </Sequence>
    <GradeBand/>
    <Interactive.Div name="Plain example disclosure" style={{position:'absolute',top:140,left:85,fontSize:36,fontWeight:400,zIndex:30}}>مثال توضيحي</Interactive.Div>
  </AbsoluteFill>;
};
