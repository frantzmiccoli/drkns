from drkns.util import get_longest_common_prefix


def test_get_longest_common_prefix():
    assert(get_longest_common_prefix([]) == '')
    assert(get_longest_common_prefix(['ok', 'ok', 'ok']) == 'ok')
    assert(get_longest_common_prefix(['good']) == 'good')
    assert(get_longest_common_prefix(
        ['miracle/good', 'miracle/divine/healing', 'miracle/divine/respawn'])
           == 'miracle/')
