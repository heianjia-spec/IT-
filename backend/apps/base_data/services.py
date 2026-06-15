"""Template merging service with tree inheritance."""

import json
from .models import AssetCategory


def get_merged_template(category: AssetCategory) -> dict:
    """
    Walk from the given category up to the root, collecting ancestor templates.
    Child fields override parent fields with the same key.
    Returns the merged template config dict.
    """
    ancestors = category.get_ancestors(include_self=True)
    merged_sections = {}

    for ancestor in ancestors:
        template = getattr(ancestor, 'form_template', None)
        if not template or not template.is_active:
            continue

        config = _parse_config(template.config)
        for section in config.get('sections', []):
            sec_name = section.get('name', '')
            if not sec_name:
                continue
            if sec_name not in merged_sections:
                merged_sections[sec_name] = {
                    'name': sec_name,
                    'sort_order': section.get('sort_order', 0),
                    'fields': {},
                }
            # Merge fields — child overrides parent by key
            for field in section.get('fields', []):
                key = field.get('key')
                if key:
                    merged_sections[sec_name]['fields'][key] = field

    # Convert field dicts back to sorted lists
    result_sections = []
    for sec in sorted(merged_sections.values(), key=lambda s: s['sort_order']):
        sorted_fields = sorted(
            sec['fields'].values(),
            key=lambda f: f.get('sort_order', 0)
        )
        result_sections.append({
            'name': sec['name'],
            'sort_order': sec['sort_order'],
            'fields': sorted_fields,
        })

    return {'sections': result_sections}


def _parse_config(config):
    """Parse template config from string or dict."""
    if isinstance(config, str):
        try:
            return json.loads(config)
        except (json.JSONDecodeError, TypeError):
            return {}
    return config or {}


def get_inheritance_chain(category: AssetCategory) -> list:
    """
    Return the inheritance chain info for a category.
    Shows which ancestors contribute fields to this category's form.
    """
    ancestors = category.get_ancestors(include_self=True)
    chain = []
    for ancestor in ancestors:
        template = getattr(ancestor, 'form_template', None)
        chain.append({
            'category_id': ancestor.id,
            'category_name': ancestor.name,
            'category_code': ancestor.code,
            'has_template': template is not None and template.is_active,
            'template_id': template.id if template else None,
            'template_name': template.name if template else None,
            'is_self': ancestor.id == category.id,
        })
    return chain
