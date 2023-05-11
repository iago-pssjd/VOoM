# File: voom_mode_r.py
# Last Modified: 2023-05-11
# Description: VOoM -- two-pane outliner plugin for Python-enabled Vim
# Website: http://www.vim.org/scripts/script.php?script_id=2657
# Author: Iago Gine-Vazquez (iago.gin-vaz AT protonmail DOT com)
# License: CC0, see http://creativecommons.org/publicdomain/zero/1.0/

"""
VOoM markup mode for R headline markup.
See |voom-mode-r|, ../../../doc/voom.txt#*voom-mode-r*

#R! headline level 1
some text
#R!! headline level 2
more text
#R!!! headline level 3
#R!!!! headline level 4

"""

import sys
if sys.version_info[0] > 2:
        xrange = range


import re

# Marker character can be changed to any ASCII character.
CHAR = '!'

# Use this if whitespace after marker chars is required.
headline_match = re.compile(r'^#R(%s+)\s' %re.escape(CHAR)).match







def hook_makeOutline(VO, blines):
    """Return (tlines, bnodes, levels) for Body lines blines.
    blines is either Vim buffer object (Body) or list of buffer lines.
    """
    Z = len(blines)
    tlines, bnodes, levels = [], [], []
    tlines_add, bnodes_add, levels_add = tlines.append, bnodes.append, levels.append
    for i in xrange(Z):
        if not blines[i].startswith('#R!'):
            continue
        bline = blines[i]
        m = headline_match(bline)
        if not m:
            continue
        lev = len(m.group(1))
        head = bline[2+lev:].strip()
        tline = '  %s|%s' %('. '*(lev-1), head)
        tlines_add(tline)
        bnodes_add(i+1)
        levels_add(lev)
    return (tlines, bnodes, levels)


def hook_newHeadline(VO, level, blnum, tlnum):
    """Return (tree_head, bodyLines).
    tree_head is new headline string in Tree buffer (text after |).
    bodyLines is list of lines to insert in Body buffer.
    """
    tree_head = 'NewHeadline'
    bodyLines = ['#R%s %s' %(CHAR * level, tree_head), '']
    return (tree_head, bodyLines)


def hook_changeLevBodyHead(VO, h, levDelta):
    """Increase of decrease level number of Body headline by levDelta."""
    if levDelta==0: return h
    m = headline_match(h)
    level = len(m.group(1))
    return '#R%s%s' %(CHAR * (level+levDelta), h[m.end(1):])

