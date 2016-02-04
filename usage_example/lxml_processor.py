"""
LXML processor, from The Atlantic's newsletter processing
"""

def remove_hr_before_native_promo(tree, sponsor_content):
    """
    sponsor_content should have a top & bottom <hr /> which is yellow.
    Since this occurs in newsletters, which must be emailed-out, this
    can't be handled via a sophisticated CSS selector.

    So, instead, we remove the previous <hr /> tag if it exists, and allow the
    sponsor-content.html template to insert it's own <hr/> before & after.

    Note: this is very sensitve to the order of transformations.
    """
    if sponsor_content:
        sponsor_dividers = tree.xpath("//hr[@class='sponsor-divider']")
        if sponsor_dividers:
            divider = sponsor_dividers[0]
            previous = divider.getparent().getprevious()
            if previous.tag == 'hr':
                parent = previous.getparent()
                parent.remove(previous)
            else:
                last_of_previous = previous[-1]
                if last_of_previous.tag == 'hr':
                    parent = last_of_previous.getparent()
                    parent.remove(last_of_previous)

def monadic_shortener(tree, sponsor_content):
    """
    ... this needs a couple of tweaked monads
    MaybeIf - a close relative of Maybe, which uses: isinstance(x, Nothing) ~ bool(x)
    ... something State related - for passing variables forward
    """
    remove = lambda element: element.getparent().remove(element)

    if sponsor_content:
        previous = (Maybe(tree)
         >> _.xpath("//hr[@class='sponsor-divider']")
         >> _[0]
         >> _.getparent().getprevious())
        previous >> Branch(
            (   continue_if(_.tag == 'hr')
                >> remove),
            (_[-1]
             >> continue_if(_.tag == 'hr')
             >> remove)
        ).first()
