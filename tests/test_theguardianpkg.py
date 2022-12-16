from theguardianpkg import theguardianpkg
import pytest

def test_search():
    example = 'https://content.guardianapis.com/film/2022/dec/15/best-films-of-2022-in-the-uk-no-7-rrr'
    expected = 'Best films of 2022 in the UK: No 7 – RRR'
    actual = theguardianpkg.single_item(example)
    assert actual == expected, "Search result is wrong."

def test_search2():
    example = 'https://content.guardianapis.com/film/2022/dec/15/obituaries-2022-olivia-newton-john-remembered-by-didi-conn-frenchy-sandy-grease'
    expected = 'Olivia Newton-John remembered by Didi Conn'
    actual = theguardianpkg.single_item(example)
    assert actual == expected, "Search result is wrong."

def test_search_mult():
    with pytest.raises(AssertionError):
        example = 'https://content.guardianapis.com/film/2022/dec/15/obituaries-2022-olivia-newton-john-remembered-by-didi-conn-frenchy-sandy-grease'
        expected = 'Title: Olivia Newton-John remembered by Didi Conn\nSection: Film\nDate: 2022-12-15T18:00:28Z\nType: article'
        actual = theguardianpkg.single_item_mult(example)
        assert actual == expected, "Search result is wrong."

