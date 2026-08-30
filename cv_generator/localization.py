from __future__ import annotations

from typing import Any

from .config import AVAILABLE_LANGUAGES, DEFAULT_LABELS


def normalize_language_value(value: Any, language: str) -> str:
    if isinstance(value, dict):
        return str(value.get(language, ""))
    if value is None:
        return ""
    return str(value)


def normalize_text_list(value: Any, language: str) -> list[str]:
    if isinstance(value, dict):
        value = value.get(language, [])

    if isinstance(value, str):
        return [value] if value else []

    if not isinstance(value, list):
        return []

    normalized_items: list[str] = []
    for item in value:
        if isinstance(item, dict):
            normalized_item = normalize_language_value(item, language)
        else:
            normalized_item = str(item)

        if normalized_item.strip():
            normalized_items.append(normalized_item)

    return normalized_items


def localize_text(value: Any, language: str) -> str:
    if isinstance(value, dict):
        if language in value:
            return localize_text(value[language], language)

        for nested_value in value.values():
            localized_value = localize_text(nested_value, language)
            if localized_value:
                return localized_value

        return ""

    if isinstance(value, list):
        items = [localize_text(item, language) for item in value]
        return " ".join(item for item in items if item).strip()

    if value is None:
        return ""

    return str(value).strip()


def localize_map(value: Any, language: str) -> dict[str, str]:
    if isinstance(value, dict) and ("pt" in value or "en" in value):
        return {
            "pt": localize_text(value.get("pt", ""), "pt"),
            "en": localize_text(value.get("en", ""), "en"),
        }

    localized_value = localize_text(value, language)
    return {"pt": localized_value, "en": localized_value}


def has_meaningful_content(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return any(has_meaningful_content(item) for item in value)
    if isinstance(value, dict):
        return any(has_meaningful_content(item) for item in value.values())
    return True


def detect_profile_languages(profile: dict[str, Any]) -> list[str]:
    detected_languages: set[str] = set()

    meta = profile.get("_meta", {})
    if isinstance(meta, dict):
        raw_meta_languages = meta.get("languages", meta.get("language"))
        if isinstance(raw_meta_languages, str):
            raw_meta_languages = [raw_meta_languages]
        if isinstance(raw_meta_languages, list):
            for language_value in raw_meta_languages:
                normalized_language = str(language_value).strip().lower()
                if normalized_language in AVAILABLE_LANGUAGES:
                    detected_languages.add(normalized_language)

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for language in AVAILABLE_LANGUAGES:
                localized_value = value.get(language)
                if has_meaningful_content(localized_value):
                    detected_languages.add(language)

            for nested_value in value.values():
                walk(nested_value)
            return

        if isinstance(value, list):
            for nested_value in value:
                walk(nested_value)

    walk(profile)
    return [language for language in AVAILABLE_LANGUAGES if language in detected_languages]


def resolve_profile_languages(
    profile: dict[str, Any],
    profile_path: Any,
    requested_languages: list[str],
    explicit_language_request: bool,
) -> list[str]:
    detected_languages = detect_profile_languages(profile)

    if not detected_languages:
        if explicit_language_request:
            detected_languages = list(requested_languages)
        else:
            detected_languages = list(AVAILABLE_LANGUAGES)
        print(
            f"⚠️  {profile_path.name}: no explicit language markers found; "
            f"using {', '.join(detected_languages)}."
        )

    if explicit_language_request:
        ignored_languages = [language for language in requested_languages if language not in detected_languages]
        for ignored_language in ignored_languages:
            print(
                f"⚠️  {profile_path.name}: requested language '{ignored_language}' "
                "was ignored (not detected in this profile)."
            )
        return [language for language in requested_languages if language in detected_languages]

    return detected_languages


def get_labels_for_language(labels_by_language: Any, language: str) -> dict[str, str]:
    if isinstance(labels_by_language, dict):
        localized_labels = labels_by_language.get(language)
        if isinstance(localized_labels, dict):
            return {str(key): str(value) for key, value in localized_labels.items()}

    return dict(DEFAULT_LABELS[language])
