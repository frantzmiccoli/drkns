from drkns.generation.templateloading.get_generation_template \
    import get_generation_template, _extract_from_tag_prefix


def test_get_generation_template():
    get_generation_template('./testprojects/nominalcase')


def test_extract_from_tag_prefix():
    faked_content = """
    Something to stay in content
    adpoj azdpoajzd paozdj azpd oj %BLOCK_BEGIN% to disappear
    Inside the block
    Inside the block x1
    Inside the block x2
    adpoj to disappear  azdpoajzd paozdj azpd oj %BLOCK_END%
    Something to stay in content 
    """

    block, new_content = _extract_from_tag_prefix('BLOCK_', faked_content)
    assert(new_content.count('stay in content') == 2)
    assert(block.count('Inside the block') == 3)

    assert (new_content.count('to disappear') == 0)
    assert (block.count('to disappear') == 0)

    assert (new_content.count('Inside the block') == 0)
    assert (block.count('in content') == 0)
