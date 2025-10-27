"""Content moderation utilities."""

import re
from typing import List, Tuple


# Basic profanity word list (expandable)
PROFANITY_WORDS = [
    "spam",
    "scam",
    "fake",
    "illegal",
    "fraud",
    "hate",
    "harassment",
    "abuse",
]


def check_profanity(text: str) -> Tuple[bool, List[str]]:
    """
    Check for profanity in text.

    Args:
        text: Text to check

    Returns:
        Tuple of (has_profanity, matched_words)
    """
    text_lower = text.lower()
    matched_words = []

    for word in PROFANITY_WORDS:
        # Check if word appears as whole word
        pattern = r"\b" + re.escape(word) + r"\b"
        if re.search(pattern, text_lower, re.IGNORECASE):
            matched_words.append(word)

    has_profanity = len(matched_words) > 0
    return has_profanity, matched_words


def check_spam_patterns(text: str) -> bool:
    """
    Check for common spam patterns.

    Args:
        text: Text to check

    Returns:
        True if spam patterns detected
    """
    spam_patterns = [
        r"\b(buy now|click here|limited time|act now)\b",
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+])+",
        r"\d{10,}",  # Long numbers (phone numbers)
        r"[A-Z]{5,}",  # All caps words
    ]

    for pattern in spam_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True

    return False


def moderate_text(text: str) -> Tuple[bool, str]:
    """
    Moderate text content.

    Args:
        text: Text to moderate

    Returns:
        Tuple of (should_flag, reason)
    """
    # Check profanity
    has_profanity, matched_words = check_profanity(text)
    if has_profanity:
        return True, f"Profanity detected: {', '.join(matched_words)}"

    # Check spam
    is_spam = check_spam_patterns(text)
    if is_spam:
        return True, "Spam patterns detected"

    return False, ""


def should_auto_flag_listing(listing) -> Tuple[bool, str]:
    """
    Check if a listing should be auto-flagged.

    Args:
        listing: Listing object to check

    Returns:
        Tuple of (should_flag, reason)
    """
    reasons = []

    # Check title
    if listing.title:
        should_flag, reason = moderate_text(listing.title)
        if should_flag:
            reasons.append(f"Title: {reason}")

    # Check description
    if listing.description:
        should_flag, reason = moderate_text(listing.description)
        if should_flag:
            reasons.append(f"Description: {reason}")

    # Check skills
    if listing.skills_required:
        for skill in listing.skills_required:
            should_flag, reason = moderate_text(str(skill))
            if should_flag:
                reasons.append(f"Skill: {reason}")

    if reasons:
        return True, "; ".join(reasons)

    return False, ""


def should_auto_flag_profile(profile) -> Tuple[bool, str]:
    """
    Check if a profile should be auto-flagged.

    Args:
        profile: Profile object to check

    Returns:
        Tuple of (should_flag, reason)
    """
    reasons = []

    # Check headline
    if profile.headline:
        should_flag, reason = moderate_text(profile.headline)
        if should_flag:
            reasons.append(f"Headline: {reason}")

    # Check bio
    if profile.bio:
        should_flag, reason = moderate_text(profile.bio)
        if should_flag:
            reasons.append(f"Bio: {reason}")

    # Check skills
    if profile.skills:
        for skill in profile.skills:
            should_flag, reason = moderate_text(str(skill))
            if should_flag:
                reasons.append(f"Skill: {reason}")

    if reasons:
        return True, "; ".join(reasons)

    return False, ""
