import React from 'react';
import {AbsoluteFill, Interactive, OffthreadVideo, Sequence, staticFile} from 'remotion';
import {BasicCaptions} from './basic-captions.element';

// Source-frame boundaries are generated and checked against public/practice/edit-plan.json.
export const PracticeCut = () => <AbsoluteFill style={{background:'#172A35',color:'white',fontFamily:'Arial, sans-serif'}}>
  <Interactive.Div name="Practice title" dir="rtl" style={{position:'absolute',top:220,left:80,right:80,fontSize:65,fontWeight:700,lineHeight:1.5}}>تمرين القص والترجمة</Interactive.Div>
  <Interactive.Div name="Fixture disclosure" dir="rtl" style={{position:'absolute',top:420,left:80,right:80,fontSize:36,color:'#b9d4cf',lineHeight:1.7}}>مقطع تجريبي وصوت اصطناعي محلي<br/>النص معروف مسبقاً — بدون تفريغ آلي</Interactive.Div>
  <Sequence from={0} durationInFrames={111} name="Take 1 — source 30 to 141">
    <OffthreadVideo src={staticFile('practice/raw-practice.mp4')} trimBefore={30} trimAfter={141} style={{position:'absolute',top:650,width:1080,height:608,objectFit:'contain'}}/>
    <Sequence from={0} durationInFrames={111} name="Caption 1">
      <BasicCaptions width={900} style={{position:'absolute',top:1350,left:90}} combineTokensWithinMilliseconds={4000} captions={[{text:'My average is only one part of my profile.',startMs:0,endMs:3700,timestampMs:null,confidence:null}]}/>
    </Sequence>
  </Sequence>
  <Sequence from={111} durationInFrames={129} name="Take 2 — source 171 to 300">
    <OffthreadVideo src={staticFile('practice/raw-practice.mp4')} trimBefore={171} trimAfter={300} style={{position:'absolute',top:650,width:1080,height:608,objectFit:'contain'}}/>
    <Sequence from={0} durationInFrames={129} name="Caption 2">
      <BasicCaptions width={900} style={{position:'absolute',top:1350,left:90}} combineTokensWithinMilliseconds={4400} captions={[{text:'Before choosing, I compare the published requirements.',startMs:0,endMs:4300,timestampMs:null,confidence:null}]}/>
    </Sequence>
  </Sequence>
  <Sequence from={240} durationInFrames={110} name="Take 3 — source 330 to 440">
    <OffthreadVideo src={staticFile('practice/raw-practice.mp4')} trimBefore={330} trimAfter={440} style={{position:'absolute',top:650,width:1080,height:608,objectFit:'contain'}}/>
    <Sequence from={0} durationInFrames={110} name="Caption 3">
      <BasicCaptions width={900} style={{position:'absolute',top:1350,left:90}} combineTokensWithinMilliseconds={4000} captions={[{text:'Then I check what each option really asks for.',startMs:0,endMs:110/30*1000,timestampMs:null,confidence:null}]}/>
    </Sequence>
  </Sequence>
  <Interactive.Div name="Audio disclosure" dir="rtl" style={{position:'absolute',bottom:210,left:80,right:80,fontSize:30,color:'#b9d4cf'}}>تجربة تقنية بالإنجليزية — ماشي فيديو إعلاني</Interactive.Div>
</AbsoluteFill>;
