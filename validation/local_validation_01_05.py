"""Local Python reference checks, not SAS execution or LLM prompt trials.

Run with the primary runtime Python (pandas and NumPy installed).
Checks example outputs, key preservation behavior, and generated module copy.
"""
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd


def main():
    print('LOCAL PYTHON REFERENCE VALIDATION: EXAMPLES 01-05')
    print(f'Python {sys.version.split()[0]}; pandas {pd.__version__}; NumPy {np.__version__}')
    print('Scope: hand-authored translations and module expected tables.')
    print('No SAS execution, no Bedrock execution, no repeated LLM trials.')
    modules = json.loads(Path(__file__).with_name('modules_01_05.json').read_text())

    # MEAN: explicit missing exclusion, all-missing stays missing, input intact.
    mean = pd.DataFrame([[1, 2, 3], [4, np.nan, 6], [np.nan]*3], columns=['x','y','z'])
    original_mean = mean.copy(deep=True)
    mean['average'] = mean[['x','y','z']].mean(axis=1, skipna=True)
    assert mean['average'].iloc[:2].tolist() == [2.0, 5.0]
    assert pd.isna(mean['average'].iloc[2])
    pd.testing.assert_frame_equal(mean[['x','y','z']], original_mean)
    assert len(mean) == 3
    assert [r[1] for r in modules[0]['expected_rows']] == ['2.0','5.0','. / NaN']
    print('PASS 01 MEAN: [2.0, 5.0, NaN]; missing cases and input preservation checked.')

    # SUBSTR: specific offsets, omitted-length behavior, and widths.
    text = pd.Series(['ABCDEFGHIJ', 'HelloWorld', 'SAS-to-Python']).str.pad(20, side='right')
    substr = pd.DataFrame({'first_three': text.str.slice(0,3),
                           'middle': text.str.slice(4,8),
                           'from_seventh': text.str.slice(6,None)})
    visible = substr.apply(lambda c: c.str.rstrip(' ')).values.tolist()
    wanted = [['ABC','EFGH','GHIJ'],['Hel','oWor','orld'],['SAS','to-P','-Python']]
    assert visible == wanted
    for col, width in [('first_three',3),('middle',4),('from_seventh',14)]:
        assert substr[col].str.len().eq(width).all()
    assert [row[1:] for row in modules[1]['expected_rows']] == wanted
    print('PASS 02 SUBSTR: all nine visible outputs; widths 3/4/14 checked.')

    # LENGTH: fixed storage, ordinary trailing blanks, all-blank returns 1.
    length_text = pd.Series(['ABC','ABC','ABCDEFGHIJ','X','']).str.pad(10, side='right')
    stored_length_text = length_text.copy()
    lengths = length_text.str.rstrip(' ').str.len().clip(lower=1)
    assert length_text.str.len().eq(10).all()
    assert lengths.tolist() == [3,3,10,1,1]
    pd.testing.assert_series_equal(length_text, stored_length_text)
    # A leading blank is meaningful, even though not an additional learner row.
    assert max(len(' ABC      '.rstrip(' ')), 1) == 4
    assert [int(row[2]) for row in modules[2]['expected_rows']] == lengths.tolist()
    print('PASS 03 LENGTH: [3, 3, 10, 1, 1]; blank case and leading-space preservation checked.')

    # CAT/CATX: missing character inputs are modeled as blanks, not dots.
    cat = pd.DataFrame([['John','Q','Public'],['Jane','','Doe'],['Bob','','Smith']],
                       columns=['first','middle','last'])
    for col in cat:
        cat[col] = cat[col].str.pad(8, side='right')
    cat['name1'] = cat['first'] + cat['middle'] + cat['last']
    cat['name2'] = cat[['first','middle','last']].apply(
        lambda row: ' '.join(v.strip(' ') for v in row if v.strip(' ')), axis=1
    ).str.pad(24, side='right')
    marked_cat = cat['name1'].str.replace(' ','_',regex=False).tolist()
    wanted_cat = ['John____Q_______Public__', 'Jane____________Doe_____',
                  'Bob_____________Smith___']
    wanted_catx = ['John Q Public','Jane Doe','Bob Smith']
    assert marked_cat == wanted_cat
    assert cat['name1'].str.len().eq(24).all()
    assert cat['name2'].str.len().eq(24).all()
    assert cat['name2'].str.rstrip(' ').tolist() == wanted_catx
    assert [row[1] for row in modules[3]['expected_rows']] == wanted_cat
    assert [row[2] for row in modules[3]['expected_rows']] == wanted_catx
    print('PASS 04 CAT/CATX: exact padded strings, blank middle fields, width 24 checked.')

    # ROUND: scope intentionally restricted to supplied non-halfway values.
    values = pd.Series([2.3,2.7,-1.4,-1.6,3.0])
    original_values = values.copy()
    rounded = values.round(0)
    assert rounded.tolist() == [2,3,-1,-2,3]
    pd.testing.assert_series_equal(values, original_values)
    assert [int(row[2]) for row in modules[4]['expected_rows']] == rounded.tolist()
    print('PASS 05 ROUND: [2, 3, -1, -2, 3]; supplied cases only, input unchanged.')
    print('RESULT: all five local reference checks passed.')
    print('Remaining: run revised SAS sources; collect independent revised A/B Bedrock trials.')


if __name__ == '__main__':
    main()
