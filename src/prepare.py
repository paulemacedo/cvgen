from __future__ import annotations

from typing import Any

from .config import DEFAULT_CONTACT
from .localization import localize_map, localize_text, normalize_language_value, normalize_text_list


def prepare_contact(profile: dict[str, Any]) -> dict[str, str]:
    contact = dict(DEFAULT_CONTACT)
    contact.update(profile.get("contact", {}))
    return {key: str(value) for key, value in contact.items()}


def prepare_experience(profile: dict[str, Any], language: str) -> list[dict[str, Any]]:
    experience_items: list[dict[str, Any]] = []
    for experience in profile.get("experience", []):
        if not isinstance(experience, dict):
            continue

        experience_items.append(
            {
                "role": localize_map(experience.get("role", ""), language),
                "company": str(experience.get("company", "")),
                "location": str(experience.get("location", "")),
                "date": localize_map(experience.get("date", ""), language),
                "bullets": normalize_text_list(experience.get("bullets", []), language),
            }
        )

    return experience_items


def prepare_education(profile: dict[str, Any], language: str) -> list[dict[str, Any]]:
    raw_education = profile.get("education", [])
    if isinstance(raw_education, dict):
        raw_education = raw_education.get(language, [])

    education_items: list[dict[str, Any]] = []
    for education in raw_education:
        if not isinstance(education, dict):
            continue

        education_items.append(
            {
                "degree": localize_map(education.get("degree", ""), language),
                "institution": str(education.get("institution", "")),
                "location": str(education.get("location", "")),
                "date": localize_map(education.get("date", education.get("expected", "")), language),
                "details": normalize_text_list(education.get("details", []), language),
            }
        )

    return education_items


def split_description_into_bullets(description: str) -> list[str]:
    description = description.strip()
    if not description:
        return []

    segments = [segment.strip() for segment in description.split(". ") if segment.strip()]
    return [segment if segment.endswith(".") else f"{segment}." for segment in segments]


def prepare_publications(profile: dict[str, Any], language: str) -> list[dict[str, Any]]:
    raw_publications = profile.get("publications", [])
    if isinstance(raw_publications, dict):
        raw_publications = raw_publications.get(language, [])

    publication_items: list[dict[str, Any]] = []
    for publication in raw_publications:
        if not isinstance(publication, dict):
            continue

        title = normalize_language_value(publication.get("title", ""), language)
        details = normalize_text_list(publication.get("details", []), language)
        description_text = normalize_language_value(publication.get("description", ""), language)

        if not details:
            details = split_description_into_bullets(description_text)

        venue = normalize_language_value(publication.get("venue", ""), language).strip()
        doi = str(publication.get("doi", "")).strip()
        doi_url = str(publication.get("doi_url", "")).strip()
        if not doi_url and doi:
            doi_url = f"https://doi.org/{doi}"

        has_explicit_details = bool(normalize_text_list(publication.get("details", []), language))
        localized_description = localize_map(publication.get("description", ""), language)
        if not has_explicit_details and details:
            localized_description = {"pt": "", "en": ""}

        publication_items.append(
            {
                "title": localize_map(publication.get("title", ""), language),
                "venue": venue,
                "date": localize_map(publication.get("date", ""), language),
                "description": localized_description,
                "details": details,
                "doi": doi,
                "doi_url": doi_url,
            }
        )

    return publication_items


def prepare_skills(profile: dict[str, Any], language: str) -> list[dict[str, Any]]:
    skill_items: list[dict[str, Any]] = []
    for skill in profile.get("skills", []):
        if not isinstance(skill, dict):
            continue

        normalized_skill = dict(skill)
        if "items" not in normalized_skill:
            normalized_skill["items"] = normalized_skill.get(f"items_{language}", [])
        if isinstance(normalized_skill.get("label"), dict):
            normalized_skill["label"] = localize_map(normalized_skill["label"], language)
        skill_items.append(normalized_skill)

    return skill_items


def prepare_projects(profile: dict[str, Any], language: str) -> list[dict[str, Any]]:
    raw_projects = profile.get("projects", [])
    if isinstance(raw_projects, dict):
        raw_projects = raw_projects.get(language, [])
    elif not isinstance(raw_projects, list):
        raw_projects = []

    project_items: list[dict[str, Any]] = []
    for project in raw_projects:
        if isinstance(project, str):
            project_items.append({"name": localize_map(project, language)})
            continue

        if isinstance(project, dict):
            subtitle = project.get("subtitle", "")
            if isinstance(subtitle, dict):
                area_key = None
                if "ti" in subtitle:
                    area_key = "ti"
                elif len(subtitle) > 0:
                    area_key = next(iter(subtitle))
                if area_key and isinstance(subtitle[area_key], dict):
                    subtitle_value = localize_map(subtitle[area_key], language)
                elif area_key:
                    subtitle_value = localize_map(subtitle[area_key], language)
                else:
                    subtitle_value = {"pt": "", "en": ""}
            else:
                subtitle_value = localize_map(subtitle, language)

            project_items.append(
                {
                    "name": localize_map(project.get("name", ""), language),
                    "subtitle": subtitle_value,
                    "description": localize_map(project.get("description", ""), language),
                    "github": str(project.get("github", "")).strip(),
                    "areas": [str(area) for area in project.get("areas", []) if str(area).strip()],
                }
            )
            continue

        project_items.append({"name": localize_map(project, language)})

    return project_items


def prepare_certifications(profile: dict[str, Any], language: str) -> list[Any]:
    raw_certifications = profile.get("certifications", [])

    if isinstance(raw_certifications, dict):
        selected_items = raw_certifications.get(language, [])
        if isinstance(selected_items, list):
            return [str(item) for item in selected_items if str(item).strip()]
        if isinstance(selected_items, str) and selected_items.strip():
            return [selected_items]
        return []

    certifications: list[Any] = []
    for certification in raw_certifications:
        if not isinstance(certification, dict):
            certification_text = str(certification).strip()
            if certification_text:
                certifications.append(certification_text)
            continue

        certifications.append(
            {
                "name": localize_map(certification.get("name", ""), language),
                "issuer": str(certification.get("issuer", "")),
                "date": localize_map(certification.get("date", ""), language),
                "details": normalize_text_list(certification.get("details", []), language),
                "hours": certification.get("hours"),
                "score": certification.get("score"),
                "url": str(certification.get("url", "")).strip(),
            }
        )

    return certifications


def render_profile(
    template: Any,
    profile: dict[str, Any],
    language: str,
    labels: dict[str, str],
    common_css_href: str,
    template_css_href: str,
) -> str:
    contact = prepare_contact(profile)
    display_name = localize_text(profile.get("name", profile.get("nome", "")), language)
    return template.render(
        lang=language,
        name=profile.get("name", profile.get("nome", {})),
        nome=display_name,
        location=profile.get("location", {}),
        location_text=localize_text(profile.get("location", {}), language),
        age_text=localize_text(profile.get("age", {}), language),
        headline=profile.get("headline", {}),
        headline_text=localize_text(profile.get("headline", {}), language),
        summary=profile.get("summary", {}),
        contact=contact,
        contact_line=" | ".join(
            [
                contact["linkedin"],
                contact["phone"],
                contact["website"],
                contact["email"],
                contact["github"],
            ]
        ),
        skills=sorted(prepare_skills(profile, language), key=lambda item: item.get("priority", 0)),
        experience=prepare_experience(profile, language),
        projects=prepare_projects(profile, language),
        education=prepare_education(profile, language),
        certifications=prepare_certifications(profile, language),
        publications=prepare_publications(profile, language),
        labels=labels,
        common_css_href=common_css_href,
        template_css_href=template_css_href,
        _meta=profile.get("_meta", {}),
    )
