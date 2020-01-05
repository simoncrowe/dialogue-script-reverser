NUMERALS = (
    '\u0030',
    '\u0031',
    '\u0032',
    '\u0033',
    '\u0034',
    '\u0035',
    '\u0036',
    '\u0037',
    '\u0038',
    '\u0039',
    '\u0061',
    '\u0062',
    '\u0063',
    '\u0064',
    '\u0065',
    '\u0066',
    '\u0067',
    '\u0068',
    '\u0069',
    '\u006A',
    '\u006B',
    '\u006C',
    '\u006D',
    '\u006E',
    '\u006F',
    '\u0070',
    '\u0071',
    '\u0072',
    '\u0073',
    '\u0074',
    '\u0075',
    '\u0076',
    '\u0077',
    '\u0078',
    '\u0079',
    '\u007A',
    '\u0041',
    '\u0042',
    '\u0043',
    '\u0044',
    '\u0045',
    '\u0046',
    '\u0047',
    '\u0048',
    '\u0049',
    '\u004A',
    '\u004B',
    '\u004C',
    '\u004E',
    '\u004F',
    '\u0050',
    '\u0051',
    '\u0052',
    '\u0053',
    '\u0054',
    '\u0055',
    '\u0056',
    '\u0057',
    '\u0058',
    '\u0059',
    '\u005A',
    '\u0023',
    '\u0024',
    '\u0025',
)
PLACE_MULTIPLIERS = (1, 64, 4096, 262144, 29986576)

def to_base_64_gen(value: int) -> str:
    remainder = value
    for place, multiplier in reversed(list(enumerate(PLACE_MULTIPLIERS))):
        if (value_at_place := int(remainder / multiplier)) != 0 or place == 0:
            yield NUMERALS[value_at_place]
            remainder %= multiplier


def base64_gen():
    counter = 0
    
    while True:
        yield ''.join(to_base_64_gen(counter))
        counter += 1

