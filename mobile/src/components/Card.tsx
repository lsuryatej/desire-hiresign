/**
 * Card Component
 * Rounded container with shadow for content cards
 */

import React from 'react';
import { View, ViewStyle, TouchableOpacity } from 'react-native';
import { theme } from '../design/theme';

interface CardProps {
  children: React.ReactNode;
  variant?: 'default' | 'outlined' | 'elevated';
  onPress?: () => void;
  style?: ViewStyle;
}

export const Card: React.FC<CardProps> = ({
  children,
  variant = 'default',
  onPress,
  style,
}) => {
  const getVariantStyle = (): ViewStyle => {
    switch (variant) {
      case 'outlined':
        return {
          borderWidth: 1,
          borderColor: theme.colors.border,
          backgroundColor: theme.colors.surface,
        };
      case 'elevated':
        return {
          backgroundColor: theme.colors.surface,
          shadowColor: '#000',
          shadowOffset: { width: 0, height: 4 },
          shadowOpacity: 0.1,
          shadowRadius: 12,
          elevation: 4,
        };
      default:
        return {
          backgroundColor: theme.colors.surface,
        };
    }
  };

  const cardStyle: ViewStyle = {
    borderRadius: theme.borderRadius.lg, // 14px rounded
    padding: theme.spacing.md,
    ...getVariantStyle(),
  };

  const content = <View style={[cardStyle, style]}>{children}</View>;

  if (onPress) {
    return (
      <TouchableOpacity onPress={onPress} activeOpacity={0.95}>
        {content}
      </TouchableOpacity>
    );
  }

  return content;
};

