/**
 * Progress Bar Component
 * Visual progress indicator for onboarding and profile completion
 */

import React from 'react';
import { View, ViewStyle } from 'react-native';
import { theme } from '../design/theme';

interface ProgressBarProps {
  progress: number; // 0-100
  height?: number;
  color?: string;
  backgroundColor?: string;
  style?: ViewStyle;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  progress,
  height = 8,
  color = theme.colors.primary,
  backgroundColor = theme.colors.bg,
  style,
}) => {
  const clampedProgress = Math.min(100, Math.max(0, progress));

  return (
    <View
      style={[
        {
          height,
          backgroundColor,
          borderRadius: theme.borderRadius.full,
          overflow: 'hidden',
        },
        style,
      ]}
    >
      <View
        style={{
          height: '100%',
          width: `${clampedProgress}%`,
          backgroundColor: color,
          borderRadius: theme.borderRadius.full,
          transition: 'width 0.2s ease',
        }}
      />
    </View>
  );
};

// Profile completion progress
export const ProfileProgressBar: React.FC<{ progress: number }> = ({
  progress,
}) => {
  return (
    <ProgressBar
      progress={progress}
      height={6}
      color={theme.colors.primary}
      backgroundColor={theme.colors.bg}
    />
  );
};

