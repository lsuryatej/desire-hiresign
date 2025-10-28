/**
 * Button Component
 * Primary and secondary button styles following design system
 */

import React from 'react';
import {
  TouchableOpacity,
  Text as RNText,
  ActivityIndicator,
  ViewStyle,
  TextStyle,
} from 'react-native';
import { theme } from '../design/theme';
import { Text } from './Text';

interface ButtonProps {
  label: string;
  onPress: () => void;
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  fullWidth?: boolean;
  style?: ViewStyle;
}

export const Button: React.FC<ButtonProps> = ({
  label,
  onPress,
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  fullWidth = false,
  style,
}) => {
  // Size styles
  const sizeStyles: { [key: string]: ViewStyle } = {
    sm: {
      paddingVertical: 8,
      paddingHorizontal: 16,
    },
    md: {
      paddingVertical: 12,
      paddingHorizontal: 24,
    },
    lg: {
      paddingVertical: 16,
      paddingHorizontal: 32,
    },
  };

  // Variant styles
  const getVariantStyle = (): ViewStyle => {
    const baseStyle: ViewStyle = {
      borderRadius: theme.borderRadius.full, // Pill shape
      alignItems: 'center',
      justifyContent: 'center',
      borderWidth: variant === 'outline' ? 2 : 0,
    };

    switch (variant) {
      case 'primary':
        return {
          ...baseStyle,
          backgroundColor: theme.colors.primary,
        };
      case 'secondary':
        return {
          ...baseStyle,
          backgroundColor: theme.colors.accent,
        };
      case 'outline':
        return {
          ...baseStyle,
          backgroundColor: 'transparent',
          borderColor: theme.colors.primary,
        };
      case 'ghost':
        return {
          ...baseStyle,
          backgroundColor: 'transparent',
        };
      default:
        return baseStyle;
    }
  };

  const textColor = variant === 'outline' || variant === 'ghost' 
    ? theme.colors.primary 
    : '#FFFFFF';

  const buttonStyle: ViewStyle = {
    ...sizeStyles[size],
    ...getVariantStyle(),
    opacity: disabled || loading ? 0.5 : 1,
    width: fullWidth ? '100%' : 'auto',
  };

  return (
    <TouchableOpacity
      style={[buttonStyle, style]}
      onPress={onPress}
      disabled={disabled || loading}
      activeOpacity={0.7}
    >
      {loading ? (
        <ActivityIndicator 
          color={textColor} 
          size="small" 
        />
      ) : (
        <Text
          weight="semibold"
          color={textColor}
        >
          {label}
        </Text>
      )}
    </TouchableOpacity>
  );
};

