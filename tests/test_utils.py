import pytest
from restfly.errors import UnexpectedValueError
from restfly.utils import dict_merge, force_case, trunc, check

def test_force_case_single():
    assert force_case('TEST', 'lower') == 'test'
    assert force_case('test', 'upper') == 'TEST'

def test_foce_case_list():
    assert force_case(['a', 'b', 'c'], 'upper') == ['A', 'B', 'C']
    assert force_case(['A', 'B', 'C'], 'lower') == ['a', 'b', 'c']

def test_dict_merge():
    assert dict_merge({'a': 1}, {'b': 2}) == {'a': 1, 'b': 2}
    assert dict_merge({'s': {'a': 1}, 'b': 2}, {'s': {'c': 3, 'a': 4}}) == {
        's': {'a': 4, 'c': 3},
        'b': 2
    }

def test_trunc():
    assert trunc('Hello There!', 128) == 'Hello There!'
    assert trunc('Too Small', 6) == 'Too...'
    assert trunc('Too Small', 3, suffix=None) == 'Too'

examples = {
    'uuid': '00000000-0000-0000-0000-000000000000',
    'email': 'someone@company.tld',
    'hex': '1234567890abcdef',
    'url': 'http://company.com/path/of/stuff',
    'ipv4': '192.168.0.1',
    'ipv6': '2001:0db8:0000:0000:0000:ff00:0042:8329'
}

def test_check_single_type():
    assert isinstance(check('test', 1, int), int)

def test_check_list_items_type():
    assert isinstance(check('test', [1, 2], list, items_type=int), list)

def test_check_single_type_softchecking():
    assert isinstance(check('test', '1', int), int)

def test_check_single_type_softcheck_fail():
    with pytest.raises(TypeError):
        check('test', '1', int, softcheck=False)

def test_check_type_fail():
    with pytest.raises(TypeError):
        check('test', 1, str)

def test_check_list_items_fail():
    with pytest.raises(TypeError):
        check('test', [1, 2, 'three'], list, items_type=int)

def test_check_list_items_softcheck():
    assert check('test', [1, 2, '3'], list, items_type=int) == [1, 2, 3]

def test_check_choices():
    check('test', [1, 2, 3], list, choices=list(range(5)))

def test_check_choices_fail():
    with pytest.raises(UnexpectedValueError):
        check('test', [1, 2, 3, 500], list, choices=list(range(5)))

def test_check_patern_mapping_uuid():
    check('test', examples['uuid'], str, pattern='uuid')

def test_check_pattern_mapping_uuid_fail():
    with pytest.raises(UnexpectedValueError):
        check('test', 'abcdef', str, pattern='uuid')

def test_check_pattern_mapping_email():
    check('test', examples['email'], str, pattern='email')

def test_check_pattern_mapping_email_fail():
    with pytest.raises(UnexpectedValueError):
        check('test', 'abcdef', str, pattern='email')

def test_check_pattern_mapping_hex():
    check('test', examples['hex'], str, pattern='hex')

def test_check_pattern_mapping_hex_fail():
    with pytest.raises(UnexpectedValueError):
        check('test', 'something', str, pattern='hex')

def test_check_pattern_mapping_url():
    check('test', examples['url'], str, pattern='url')

def test_check_pattern_mapping_url_fail():
    with pytest.raises(UnexpectedValueError):
        check('test', 'abcdef', str, pattern='url')

def test_check_pattern_mapping_ipv4():
    check('test', examples['ipv4'], str, pattern='ipv4')

def test_check_pattern_mapping_ipv4_fail():
    with pytest.raises(UnexpectedValueError):
        check('test', 'abcdef', str, pattern='ipv4')

def test_check_pattern_mapping_ipv6():
    check('test', examples['ipv6'], str, pattern='ipv6')

def test_check_pattern_mapping_ipv6_fail():
    with pytest.raises(UnexpectedValueError):
        check('test', 'abcdef', str, pattern='ipv6')

def test_check_regex_pattern():
    check('test', '12345', str, regex=r'^\d+$')

def test_check_regex_fail():
    with pytest.raises(UnexpectedValueError):
        check('test', 'abcdef', str, regex=r'^\d+$')