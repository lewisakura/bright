# Derived from mkdocs-material's shortcodes: https://raw.githubusercontent.com/squidfunk/mkdocs-material/3cc0a30f6735e71a9f9262dc871419f7792628e5/src/overrides/hooks/shortcodes.py

import posixpath
import re

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import File, Files
from mkdocs.structure.pages import Page

from textwrap import dedent
from re import Match

def on_page_markdown(
	markdown: str, *, page: Page, config: MkDocsConfig, files: Files
):
	# Replace callback
	def replace(match: Match):
		type, args = match.groups()
		args = args.strip()

		if type == "version":        return _badge_for_version(args, page, files)
		elif type == "construction": return _under_construction()
		elif type == "bright-dev":   return _guide_for_bright_dev(page, files)

		# Otherwise, raise an error
		raise RuntimeError(f"Unknown shortcode: {type}")

	# Find and replace all external asset URLs in current page
	return re.sub(
		r"<!-- b:([\w-]+)(.*?) -->",
		replace, markdown, flags = re.I | re.M
	)

# -----------------------------------------------------------------------------

# Resolve path of file relative to given page - the posixpath always includes
# one additional level of `..` which we need to remove
def _resolve_path(path: str, page: Page, files: Files):
	path, anchor, *_ = f"{path}#".split("#")
	path = _resolve(files.get_file_from_path(path), page)
	return "#".join([path, anchor]) if anchor else path

# Resolve path of file relative to given page - the posixpath always includes
# one additional level of `..` which we need to remove
def _resolve(file: File, page: Page):
	path = posixpath.relpath(file.src_uri, page.file.src_uri)
	return posixpath.sep.join(path.split(posixpath.sep)[1:])

# -----------------------------------------------------------------------------

# Create badge
def _badge(icon: str, text: str = "", type: str = ""):
	classes = f"mdx-badge mdx-badge--{type}" if type else "mdx-badge"
	return "".join([
		f"<span class=\"{classes}\">",
		*([f"<span class=\"mdx-badge__icon\">{icon}</span>"] if icon else []),
		*([f"<span class=\"mdx-badge__text\">{text}</span>"] if text else []),
		f"</span>",
	])

# Create badge for version
def _badge_for_version(text: str, page: Page, files: Files):
	spec = text

	# Return badge
	icon = "material-tag-outline"
	href = _resolve_path("badges.md#version", page, files)
	changelog = _resolve_path("changelog.md#" + spec, page, files)
	return _badge(
		icon = f"[:{icon}:]({href} 'Minimum version')",
		text = f"[{text}]({changelog})" if spec else ""
	)

# -----------------------------------------------------------------------------

# Under construction admonition
def _under_construction():
	return dedent("""
	!!! workshop "This part of the documentation is currently under construction."
	""")

def _guide_for_bright_dev(page: Page, files: Files):
	href = _resolve_path("developer-guide/index.md", page, files)

	return dedent(f"""
	!!! info

		This part of the documentation is for the development of Bright itself. If this is not what you are looking for,
		go to the [developer guide index]({href}) to find the correct information.
	""")
