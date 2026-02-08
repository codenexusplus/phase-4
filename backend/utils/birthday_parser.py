import re
from datetime import datetime
from typing import List, Tuple, Optional

def extract_birthdays_from_text(text: str) -> List[Tuple[str, str]]:
    """
    Extracts birthday information from text.
    
    Args:
        text: The text to parse for birthday information
        
    Returns:
        List of tuples containing (person_name, date_string)
    """
    # Patterns to match birthday information
    patterns = [
        # Matches: "John Doe's birthday is on March 15" or "John Doe's birthday: March 15"
        r"([A-Za-z\s]+)'s\s+birthday\s+(?:is\s+on|on|:)\s+([A-Za-z]+\s+\d{1,2})",
        
        # Matches: "birthday of John Doe is March 15"
        r"birthday\s+of\s+([A-Za-z\s]+)\s+is\s+([A-Za-z]+\s+\d{1,2})",
        
        # Matches: "John Doe - birthday March 15"
        r"([A-Za-z\s]+)\s*[-â€“â€”]\s*birthday\s+([A-Za-z]+\s+\d{1,2})",
        
        # Matches: "John Doe (birthday: March 15)"
        r"([A-Za-z\s]+)\s*\(?birthday\s*[:\-]\s*([A-Za-z]+\s+\d{1,2})\)?",
        
        # Matches: "March 15 - John Doe's birthday"
        r"([A-Za-z]+\s+\d{1,2})\s*[-â€“â€”]\s*([A-Za-z\s]+)'s\s+birthday",
    ]
    
    birthdays = []
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if len(match) == 2:
                # Determine which element is the name and which is the date
                # Usually the first element is the name, second is the date
                # But in some patterns it's reversed
                if is_date_format(match[0]):
                    # Date comes first in this pattern
                    date_str, name = match
                else:
                    # Name comes first in this pattern
                    name, date_str = match
                
                # Normalize the name and date
                name = name.strip()
                date_str = normalize_date_format(date_str.strip())
                
                if name and date_str:
                    birthdays.append((name, date_str))
    
    return birthdays

def is_date_format(text: str) -> bool:
    """
    Checks if a string looks like a date format.
    
    Args:
        text: String to check
        
    Returns:
        True if the string looks like a date, False otherwise
    """
    # Common month names
    months = [
        "january", "february", "march", "april", "may", "june",
        "july", "august", "september", "october", "november", "december",
        "jan", "feb", "mar", "apr", "jun", "jul", "aug", "sep", "oct", "nov", "dec"
    ]
    
    text_lower = text.lower()
    
    # Check if it contains a month name and a day number
    has_month = any(month in text_lower for month in months)
    has_day = bool(re.search(r'\b\d{1,2}\b', text))
    
    return has_month and has_day

def normalize_date_format(date_str: str) -> Optional[str]:
    """
    Normalizes a date string to a consistent format (Month Day).
    
    Args:
        date_str: Date string to normalize
        
    Returns:
        Normalized date string or None if invalid
    """
    # Common month names with abbreviations
    month_map = {
        "january": "January", "jan": "January",
        "february": "February", "feb": "February",
        "march": "March", "mar": "March",
        "april": "April", "apr": "April",
        "may": "May",
        "june": "June",
        "july": "July",
        "august": "August", "aug": "August",
        "september": "September", "sep": "September", "sept": "September",
        "october": "October", "oct": "October",
        "november": "November", "nov": "November",
        "december": "December", "dec": "December",
    }
    
    # Split the date string
    parts = date_str.split()
    if len(parts) < 2:
        return None
    
    month_part = parts[0].lower()
    day_part = parts[1]
    
    # Validate and normalize the month
    if month_part not in month_map:
        return None
    
    normalized_month = month_map[month_part]
    
    # Validate the day
    try:
        day = int(day_part)
        if day < 1 or day > 31:
            return None
    except ValueError:
        return None
    
    return f"{normalized_month} {day}"

def find_birthday_by_date(birthdays: List[Tuple[str, str]], target_date: str) -> List[str]:
    """
    Finds people whose birthday matches the target date.
    
    Args:
        birthdays: List of (name, date) tuples
        target_date: Target date to search for
        
    Returns:
        List of names whose birthday matches the target date
    """
    matching_names = []
    normalized_target = normalize_date_format(target_date)
    
    if not normalized_target:
        return []
    
    for name, date in birthdays:
        normalized_date = normalize_date_format(date)
        if normalized_date and normalized_date.lower() == normalized_target.lower():
            matching_names.append(name)
    
    return matching_names

def find_birthdays_on_specific_date(text: str, target_date: str) -> List[str]:
    """
    Finds people whose birthday matches the target date from the given text.
    
    Args:
        text: Text to search for birthday information
        target_date: Target date to search for (e.g., "August 14")
        
    Returns:
        List of names whose birthday matches the target date
    """
    birthdays = extract_birthdays_from_text(text)
    return find_birthday_by_date(birthdays, target_date)
