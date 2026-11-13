import React from 'react';
import {
  AbsoluteFill,
  Easing,
  Interactive,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

type Props = {
  title: string;
  subtitle: string;
  accent: string;
};

const AnimatedTitle = ({title}: {title: string}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  return (
    <Interactive.Div
      name="Arabic title"
      dir="rtl"
      lang="ar"
      style={{
        fontSize: 108,
        fontWeight: 700,
        lineHeight: 1.5,
        textAlign: 'center',
        opacity: interpolate(frame, [0, 0.6 * fps], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        }),
        translate: interpolate(frame, [0, 0.6 * fps], ['0px 48px', '0px 0px'], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: Easing.bezier(0.16, 1, 0.3, 1),
        }),
      }}
    >
      {title}
    </Interactive.Div>
  );
};

export const InstallationCheck = ({title, subtitle, accent}: Props) => (
  <AbsoluteFill
    dir="rtl"
    lang="ar"
    style={{
      backgroundColor: '#172a35',
      color: '#ffffff',
      fontFamily: 'Arial, sans-serif',
      padding: 100,
      justifyContent: 'center',
      gap: 44,
    }}
  >
    <Interactive.Div
      name="Diagnostic label"
      style={{fontSize: 38, color: '#b6c8d0', textAlign: 'center'}}
    >
      تجربة تقنية للمحرك
    </Interactive.Div>
    <AnimatedTitle title={title} />
    <Interactive.Div
      name="Accent divider"
      style={{width: 140, height: 8, backgroundColor: accent, alignSelf: 'center'}}
    />
    <Interactive.Div
      name="Arabic subtitle"
      style={{fontSize: 52, textAlign: 'center', lineHeight: 1.6}}
    >
      {subtitle}
    </Interactive.Div>
    <Interactive.Div
      name="Duration note"
      style={{fontSize: 34, color: '#b6c8d0', textAlign: 'center', marginTop: 80}}
    >
      ثلاث ثواني بدون صوت
    </Interactive.Div>
  </AbsoluteFill>
);
