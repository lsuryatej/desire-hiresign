/**
 * Tag Component
 * Pill-shaped tags for skills, filters, and labels
 */

import React from 'react';
import { View, ViewStyle } from 'react-native';
import { theme } from '../design/theme';
import { Text } from './Text';

interface TagProps {
  label: string;
  variant?: 'default' | 'primary' | 'accent' | 'outline';
  size?: 'sm' | 'md';
  onPress?: () => void;
  style?: ViewStyle;
}

export const Tag: React.FC<TagProps> = ({
  label,
  variant = 'default',
  size = 'md',
  onPress,
  style,
}) => {
  const getVariantStyle = (): ViewStyle => {
    switch (variant) {
      case 'primary':
        return {
          backgroundColor: theme.colors.primary + '15', // 15% opacity
        };
      case 'accent':
        return {
          backgroundColor: theme.colors.accent + '15',
        };
      case 'outline':
        return {
          backgroundColor: 'transparent',
          borderWidth: 1,
          borderColor: theme.colors.border,
        };
      default:
        return {
          backgroundColor: theme.colors.bg,
        };
    }
  };

  const getTextColor = (): string => {
    switch (variant) {
      case 'primary':
        return theme.colors.primary;
      case 'accent':
        return theme.colors.accent;
      default:
        return theme.colors.text;
    }
  };

  const padding = size === 'sm' 
    ? { paddingVertical: 4, paddingHorizontal: 12 }
    : { paddingVertical: 6, paddingHorizontal: 16 };

  const tagStyle: ViewStyle = {
    borderRadius: theme.borderRadius.full,
    alignSelf: 'flex-start',
    ...padding,
    ...getVariantStyle(),
  };

  return (
    <View style={[tagStyle, style]} onTouchEnd={onPress}>
      <Text size={size === 'sm' ? 'xs' : 'sm'} color={getTextColor()}>
        {label}
      </Text>
    </View>
  );
};

// Skills tag component
export const SkillTag: React.FC<TagProps> = (props) => {
  return <Tag variant="accent" size="md" {...props} />;
};

// Filter tag component
export const FilterTag: React.FC<TagProps & { active?: boolean }> = ({
  active,
  ...props
}) => {
  return (
    <Tag
      variant={active ? 'primary' : 'outline'}
      size="md"
      {...props}
    />
  );
};

