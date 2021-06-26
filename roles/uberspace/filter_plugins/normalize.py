from typing import Callable
from collections.abc import Iterable
from typing import Any, Union, Optional
from types import FunctionType
from ansible.plugins.lookup.password import LookupModule as Password
from ansible.parsing.dataloader import DataLoader


class FilterModule(object):
    ''' jinja2 filters '''
    pw = Password(DataLoader())

    def filters(self):
        return {
            'normalize_item_to_dict': self.normalize_item_to_dict,
            'normalize_items_to_dicts': self.normalize_items_to_dicts,
            'normalize_mailboxes': self.normalize_mailboxes,
        }

    def normalize_items_to_dicts(self, items: Iterable, default_key: str, additional_keys: Optional[Iterable[Union[str,Iterable[str,Any]]]]):
        def per_item(x):
            return self.normalize_item_to_dict(x, default_key, additional_keys)

        return type(items)(map(per_item, items))

    def normalize_item_to_dict(self, item: Any, default_key: str, additional_keys: Optional[Iterable[Union[str,Iterable[str,Any]]]]):
        """
        Apply python string formatting on an object:
        .. sourcecode:: jinja
            {{ "%s - %s"|format("Hello?", "Foo!") }}
                -> Hello? - Foo!
        """
        out = dict()
        attrs = additional_keys or []

        #print('normalize_item_to_dict() type(item) is {} (isinstance(item, dict) is {})'.format(type(item), isinstance(item, dict)))
        if not isinstance(item, dict):
            out[default_key] = item
            #print('normalize_item_to_dict() out set to {}'.format(out))
        else:
            attrs = [default_key] + attrs

        for additional in attrs:
            key = additional if isinstance(additional, str) else additional[0]
            val = None if isinstance(additional, str) else additional[1]

            if isinstance(val, FunctionType):
                try:
                    val = val()
                except Exception as e:
                    print('[{}.{}] running function failed! {}'.format(item, key, e))
                    pass

            out[key] = item[key] if key in item else val

        return out

    def normalize_mailboxes(self, items: Iterable[Union[str,tuple[str,Any]]], password_spec='/dev/null chars=ascii_letters,digits,.:;-_$%&=# length=16'):
        return self.normalize_items_to_dicts(items, 'name', [('password', lambda: self.pw.run([password_spec], [])[0]), ('simple_rules', None)])
