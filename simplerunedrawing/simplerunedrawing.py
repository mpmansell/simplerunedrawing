"""SimpleRuneDrawing - Module for drawing and representing Elder Futhark runes.

This module provides functionality for randomly generating rune draws and converting
them to their string representations. It supports both upright and reversed orientations
for the 24 runes of the Elder Futhark alphabet.

Functions:
    draw_runes: Generate a random draw of runes with their orientations.
    runes_to_string: Convert rune tuples to human-readable string representations.
"""

from annotationlib import __all__
from typing import List, Tuple 
import random 

__all__ = ["draw_runes", "runes_to_string", "RUNES"]


# List of Elder Futhark runes        
RUNES: list = [
    "Ansuz", "Beorc", "Daeg", "Ehwaz", "Eiwaz", "Eohl", "Fehu", "Gifu",
    "Hagall", "Ing", "Isa", "Jera", "Kenaz", "Lagaz", "Mannaz", "Nied",
    "Othel", "Perdhro", "Raido", "Sigel", "Thurisaz", "Tir", "Uruz","Wunjo"
    ]

# Sides for rune orientation
Sides: List[str] = ["", "reversed_"]


def draw_runes(num_runes: int) -> List[Tuple[int, int]]:
    """Generate a random draw of Elder Futhark runes with orientations.
    
    Randomly selects the specified number of runes from the 24 runes of the Elder Futhark
    alphabet and assigns each rune an orientation (upright or reversed).
    
    Args:
        num_runes: The number of runes to draw. Must be between 1 and 24.
        
    Returns:
        A list of tuples where each tuple contains (orientation, rune_index).
        orientation is 0 for upright or 1 for reversed.
        rune_index is an integer between 0 and 23 representing the rune.
    """
    
    return list(zip(random.choices([0,1],k=num_runes), random.sample(range(24), num_runes)))


def runes_to_string(runes: List[Tuple[int, int]]) -> List[str]:
    """Convert rune tuples to their human-readable string representations.
    
    Translates numeric rune and orientation values into readable string names,
    with "Reversed" prefix applied to inverted runes.
    
    Args:
        runes: A list of tuples where each tuple is (orientation, rune_index).
            orientation: 0 for upright, 1 for reversed.
            rune_index: Integer between 0 and 23 representing the rune.
            
    Returns:
        A list of strings with the names of the runes, prefixed with "Reversed "
        for inverted runes (e.g., ["Fehu", "Reversed Ansuz", "Beorc"]).
    """
    
    return [f"{Sides[side]}{RUNES[rune]}" for side, rune in runes]  


