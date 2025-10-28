/**
 * Text Component
 * Typography system with consistent styling
 */

import React from 'react';
import { Text as RNText, TextStyle, StyleSheet } from 'react-native';
import { theme } from '../design/theme';

interface TextProps {
  children: React.ReactNode;
  size?: keyof typeof theme.typography.fontSize;
  weight?: keyof typeof theme.typography.fontWeight;
  color?: string;
  align?: 'left' | 'center' | 'right';
  style?: TextStyle;
}

export const Text: React.FC<TextProps> = ({
  children,
  size = 'base',
  weight = 'normal',
  color = theme.colors.text,
  align = 'left',
  style,
}) => {
  const textStyle: TextStyle = {
    fontFamily: theme.typography.fontFamily.base,
    fontSize: parseInt(theme.typography.fontSize[size]),
    fontWeight: theme.typography.fontWeight[weight],
    color,
    textAlign: align,
    lineHeight: theme.typography.lineHeight.normal,
  };

  return <RNText style={[textStyle, style]}>{children}</RNText>;
};

// Heading component variants
export const Heading: React.FC<TextProps & { level?: 1 | 2 | 3 | 4 }> = ({
  children,
  level = 2,
  weight = 'semibold',
  color = theme.colors.text,
  align = 'left',
  style,
}) => {
  const sizes: { [key: number]: keyof typeof theme.typography.fontSize } = {
    1: '3xl',
    2: '2xl',
    3: 'xl',
    4: 'lg',
  };

  return (
    <Text
      size={sizes[level]}
      weight={weight}
      color={color}
      align={align}
      style={style}
    >
      {children}
    </Text>
  );
};

// Muted text variant
export const MutedText: React.FC<TextProps> = ({ children, style }) => {
  return (
    <Text color={theme.colors.muted} style={style}>
      {children}
    </Text>
  );
};

// Semantic text variants
export const SuccessText: React.FC<TextProps> = ({ children, style }) => {
  return (
    <Text color={theme.colors.success} style={style}>
      {children}
    </Text>
  );
};

export const ErrorText: React.FC<TextProps> = ({ children, style }) => {
  return (
    <Text color={theme.colors.error} style={style}>
      {children}
    </Text>
  );
};

