#!/usr/bin/env python'
""" List of all the available XSL-FO attributes"""

XSL_FO_ATTRIBUTES = [
    'source-document',
    'role',
    'absolute-position',
    'top',
    'right',
    'bottom',
    'left',
    'azimuth',
    'cue-after',
    'cue-before',
    'elevation',
    'pause-after',
    'pause-before',
    'pitch',
    'pitch-range',
    'play-during',
    'richness',
    'speak',
    'speak-header',
    'speak-numeral',
    'speak-punctuation',
    'speech-rate',
    'stress',
    'voice-family',
    'volume',
    'background-attachment',
    'background-color',
    'background-image',
    'background-repeat',
    'background-position-horizontal',
    'background-position-vertical',
    'border-before-color',
    'border-before-style',
    'border-before-width',
    'border-after-color',
    'border-after-style',
    'border-after-width',
    'border-start-color',
    'border-start-style',
    'border-start-width',
    'border-end-color',
    'border-end-style',
    'border-end-width',
    'border-top-color',
    'border-top-style',
    'border-top-width',
    'border-bottom-color',
    'border-bottom-style',
    'border-bottom-width',
    'border-left-color',
    'border-left-style',
    'border-left-width',
    'border-right-color',
    'border-right-style',
    'border-right-width',
    'padding-before',
    'padding-after',
    'padding-start',
    'padding-end',
    'padding-top',
    'padding-bottom',
    'padding-left',
    'padding-right',
    'Fonts and Font Data',
    'font-family',
    'font-selection-strategy',
    'font-size',
    'font-stretch',
    'font-size-adjust',
    'font-style',
    'font-variant',
    'font-weight',
    'country',
    'language',
    'script',
    'hyphenate',
    'hyphenation-character',
    'hyphenation-push-character-count',
    'hyphenation-remain-character-count',
    'margin-top',
    'margin-bottom',
    'margin-left',
    'margin-right',
    'space-before',
    'space-after',
    'start-indent',
    'end-indent',
    'margin-top',
    'margin-bottom',
    'margin-left',
    'margin-right',
    'space-end',
    'space-start',
    'top',
    'right',
    'bottom',
    'left',
    'relative-position',
    'alignment-adjust',
    'alignment-baseline',
    'baseline-shift',
    'display-align',
    'dominant-baseline',
    'relative-align',
    'allowed-height-scale',
    'allowed-width-scale',
    'block-progression-dimension',
    'content-height',
    'content-width',
    'height',
    'inline-progression-dimension',
    'max-height',
    'max-width',
    'min-height',
    'min-width',
    'scaling',
    'scaling-method',
    'width',
    'hyphenation-keep',
    'hyphenation-ladder-count',
    'last-line-end-indent',
    'line-height',
    'line-height-shift-adjustment',
    'line-stacking-strategy',
    'linefeed-treatment',
    'white-space-treatment',
    'text-align',
    'text-align-last',
    'text-indent',
    'white-space-collapse',
    'wrap-option',
    'character',
    'letter-spacing',
    'suppress-at-line-break',
    'text-decoration',
    'text-shadow',
    'text-transform',
    'treat-as-word-space',
    'word-spacing',
    'color',
    'color-profile-name',
    'rendering-intent',
    'clear',
    'float',
    'intrusion-displace',
    'break-after',
    'break-before',
    'keep-together',
    'keep-with-next',
    'keep-with-previous',
    'orphans',
    'widows',
    'clip',
    'overflow',
    'reference-orientation',
    'span',
    'leader-alignment',
    'leader-pattern',
    'leader-pattern-width',
    'leader-length',
    'rule-style',
    'rule-thickness',
    'active-state',
    'auto-restore',
    'case-name',
    'case-title',
    'destination-placement-offset',
    'external-destination',
    'indicate-destination',
    'internal-destination',
    'show-destination',
    'starting-state',
    'switch-to',
    'target-presentation-context',
    'target-processing-context',
    'target-stylesheet',
    'index-class',
    'index-key',
    'page-number-treatment',
    'merge-ranges-across-index-key-references',
    'merge-sequential-page-numbers',
    'merge-pages-across-index-key-references',
    'ref-index-key',
    'marker-class-name',
    'retrieve-boundary-within-table',
    'retrieve-class-name',
    'retrieve-position',
    'retrieve-boundary',
    'retrieve-position-within-table',
    'format',
    'grouping-separator',
    'grouping-size',
    'letter-value',
    'blank-or-not-blank',
    'column-count',
    'column-gap',
    'extent',
    'flow-name',
    'force-page-count',
    'initial-page-number',
    'master-name',
    'master-reference',
    'maximum-repeats',
    'media-usage',
    'odd-or-even',
    'page-height',
    'page-position',
    'page-width',
    'precedence',
    'region-name',
    'flow-map-name',
    'flow-map-reference',
    'flow-name-reference',
    'region-name-reference',
    'border-after-precedence',
    'border-before-precedence',
    'border-collapse',
    'border-end-precedence',
    'border-separation',
    'border-start-precedence',
    'caption-side',
    'column-number',
    'column-width',
    'empty-cells',
    'ends-row',
    'number-columns-repeated',
    'number-columns-spanned',
    'number-rows-spanned',
    'starts-row',
    'table-layout',
    'table-omit-footer-at-break',
    'table-omit-header-at-break',
    'direction',
    'glyph-orientation-horizontal',
    'glyph-orientation-vertical',
    'text-altitude',
    'text-depth',
    'unicode-bidi',
    'writing-mode',
    'change-bar-class',
    'change-bar-color',
    'change-bar-offset',
    'change-bar-placement',
    'change-bar-style',
    'change-bar-width',
    'content-type',
    'id',
    'intrinsic-scale-value',
    'page-citation-strategy',
    'provisional-label-separation',
    'provisional-distance-between-starts',
    'ref-id',
    'scale-option',
    'score-spaces',
    'src',
    'visibility',
    'z-index',
    'background',
    'background-position',
    'border',
    'border-bottom',
    'border-color',
    'border-left',
    'border-right',
    'border-style',
    'border-spacing',
    'border-top',
    'border-width',
    'cue',
    'font',
    'margin',
    'padding',
    'page-break-after',
    'page-break-before',
    'page-break-inside',
    'pause',
    'position',
    'size',
    'vertical-align',
    'white-space',
    'xml:lang',
]
