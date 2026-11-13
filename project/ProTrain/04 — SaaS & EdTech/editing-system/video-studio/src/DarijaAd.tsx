import React, {useEffect, useState} from 'react';
import {Audio} from '@remotion/media';
import {AbsoluteFill, Easing, Img, Interactive, Sequence, cancelRender, continueRender, delayRender, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';

const green='#0A6B43';
const amber='#F2A541';
const forest='#0F2A1F';
const ivory='#F6F4EE';
const clamp={extrapolateLeft:'clamp',extrapolateRight:'clamp'} as const;
const settle={...clamp,easing:Easing.bezier(.16,1,.3,1)};
let fontPromise: Promise<FontFace> | undefined;

const useCairo = () => {
  const [handle]=useState(()=>delayRender('Loading the original ProTrain Cairo Arabic font'));
  useEffect(()=>{
    if(!fontPromise){
      const font=new FontFace('ProTrain Cairo',`url("${staticFile('darija-ad/cairo-arabic.woff2')}")`,{weight:'200 1000'});
      fontPromise=font.load().then(loaded=>{document.fonts.add(loaded);return loaded;});
    }
    fontPromise.then(()=>continueRender(handle)).catch(cancelRender);
  },[handle]);
};

const StudentPhoto = () => {
  const frame=useCurrentFrame();
  const {fps}=useVideoConfig();
  return <Img src={staticFile('darija-ad/student-at-desk.png')} style={{width:1080,height:1920,objectFit:'cover',
    scale:interpolate(frame,[0,2*fps],[1,1.025],clamp),transformOrigin:'58% 54%'}}/>;
};

const Hook = () => {
  const frame=useCurrentFrame();
  const {fps}=useVideoConfig();
  return <AbsoluteFill>
    <StudentPhoto/>
    <Interactive.Div name="Opening question" style={{position:'absolute',top:282,right:145,left:85,fontSize:86,lineHeight:1.5,fontWeight:750,textAlign:'right',color:forest}}>كتوجد</Interactive.Div>
    <Interactive.Div name="Campus France hook strip" style={{position:'absolute',top:425,left:74,right:136,padding:'6px 25px 20px',backgroundColor:green,color:ivory,fontSize:89,lineHeight:1.5,fontWeight:850,textAlign:'center',
      rotate:interpolate(frame,[0,.3*fps],['-2.5deg','-1.5deg'],settle),
      translate:interpolate(frame,[0,.3*fps],['0px 12px','0px 0px'],settle)}}>لكامبوس فرانس؟</Interactive.Div>
  </AbsoluteFill>;
};

const Matching = () => {
  const frame=useCurrentFrame();
  const {fps}=useVideoConfig();
  return <AbsoluteFill>
    <Img src={staticFile('craft/desk-photographic-protrain-v2.png')} style={{width:1080,height:1920,objectFit:'cover',
      scale:interpolate(frame,[0,3.4*fps],[1.045,1],clamp),transformOrigin:'50% 65%'}}/>
    <Interactive.Div name="Product name" style={{position:'absolute',top:317,right:150,left:100,fontSize:54,fontWeight:700,lineHeight:1.6,textAlign:'right',color:forest}}>بروترين ماتش</Interactive.Div>
    <Interactive.Div name="Personalized formations headline" style={{position:'absolute',top:513,left:80,right:155,padding:'0px 35px 16px',backgroundColor:green,color:ivory,fontSize:114,fontWeight:850,lineHeight:1.5,textAlign:'right',rotate:'-2deg',
      translate:interpolate(frame,[0,.28*fps],['0px 30px','0px 0px'],settle)}}>تكوينات</Interactive.Div>
    <Interactive.Div name="Academic profile benefit" style={{position:'absolute',top:745,right:146,left:90,fontSize:84,fontWeight:800,lineHeight:1.55,textAlign:'right',color:forest,
      translate:interpolate(frame,[0,.3*fps],['0px 22px','0px 0px'],settle)}}>على حساب ملفك</Interactive.Div>
    <Interactive.Div name="Amber editorial underline" style={{position:'absolute',top:903,right:150,width:470,height:13,backgroundColor:amber,rotate:'-2deg',
      scale:interpolate(frame,[0,.38*fps],[.8,1],settle),transformOrigin:'right center'}}/>
  </AbsoluteFill>;
};

const Action = () => {
  const frame=useCurrentFrame();
  const {fps}=useVideoConfig();
  return <AbsoluteFill>
    <Img src={staticFile('darija-ad/student-at-desk.png')} style={{width:1080,height:1920,objectFit:'cover',scale:1.08,transformOrigin:'57% 43%'}}/>
    <Interactive.Div name="CTA green field" style={{position:'absolute',left:0,right:0,top:1210,bottom:0,backgroundColor:green,
      translate:interpolate(frame,[0,.23*fps],['0px 38px','0px 0px'],settle)}}/>
    <Interactive.Div name="CTA product name" style={{position:'absolute',top:1261,left:100,right:145,fontSize:52,fontWeight:650,lineHeight:1.6,textAlign:'center',color:ivory}}>بروترين ماتش</Interactive.Div>
    <Interactive.Div name="Complete your academic profile" style={{position:'absolute',top:1398,left:95,right:145,padding:'10px 22px 24px',fontSize:88,fontWeight:850,lineHeight:1.45,textAlign:'center',backgroundColor:amber,color:forest,rotate:'-1deg',
      translate:interpolate(frame,[0,.23*fps],['0px 38px','0px 0px'],settle)}}>عمّر ملفك دابا</Interactive.Div>
  </AbsoluteFill>;
};

export const DarijaAd = () => {
  useCairo();
  const {fps}=useVideoConfig();
  return <AbsoluteFill dir="rtl" lang="ar-MA" style={{fontFamily:'ProTrain Cairo, sans-serif',backgroundColor:ivory,color:forest}}>
    <Audio src={staticFile('darija-ad/voice-final.wav')}/>
    <Sequence from={0} durationInFrames={2*fps} name="Recognize the Campus France question"><Hook/></Sequence>
    <Sequence from={2*fps} durationInFrames={3.4*fps} name="Recommendations based on your academic profile"><Matching/></Sequence>
    <Sequence from={5.4*fps} durationInFrames={4.1*fps} name="Complete your profile — held CTA"><Action/></Sequence>
    <Interactive.Div name="Original ProTrain company logo" style={{position:'absolute',left:78,top:116,width:158,height:158,backgroundColor:ivory,borderRadius:79,display:'flex',alignItems:'center',justifyContent:'center'}}>
      <Img src={staticFile('darija-ad/protrain-logo-site.png')} style={{width:132,height:132,objectFit:'contain'}}/>
    </Interactive.Div>
  </AbsoluteFill>;
};
