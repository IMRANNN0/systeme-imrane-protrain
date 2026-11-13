import React from 'react';
import {Composition} from 'remotion';
import {InstallationCheck} from './InstallationCheck';
import {PracticeComparison} from './PracticeComparison';
import {PracticeCut} from './PracticeCut';
import {PracticeComparisonV2} from './PracticeComparisonV2';
import {CraftStudy} from './CraftStudy';
import {DarijaAd} from './DarijaAd';
import {Pilot001, loadPilot001Plan} from './Pilot001';

export const VideoRoot = () => (
  <>
  <Composition
    id="InstallationCheck"
    component={InstallationCheck}
    durationInFrames={90}
    fps={30}
    width={1080}
    height={1920}
    defaultProps={{
      title: 'اختبار المونتاج',
      subtitle: 'الحركة والكتابة بالعربية',
      accent: '#4dd3b0',
    }}
  />
  <Composition id="PracticeComparison" component={PracticeComparison} durationInFrames={540} fps={30} width={1080} height={1920}/>
  <Composition id="PracticeCut" component={PracticeCut} durationInFrames={350} fps={30} width={1080} height={1920}/>
  <Composition id="PracticeComparisonV2" component={PracticeComparisonV2} durationInFrames={540} fps={30} width={1080} height={1920}/>
  <Composition id="CraftStudy" component={CraftStudy} durationInFrames={270} fps={30} width={1080} height={1920}/>
  <Composition id="DarijaAd" component={DarijaAd} durationInFrames={285} fps={30} width={1080} height={1920}/>
  <Composition id="Pilot001" component={Pilot001} durationInFrames={1140} fps={30} width={1080} height={1920}
    calculateMetadata={async () => { const plan = await loadPilot001Plan(); return {durationInFrames:plan.durationInFrames, fps:plan.fps, width:plan.width, height:plan.height}; }}/>
  </>
);
