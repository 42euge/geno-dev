---
name: autocad-drawing
description: >-
  Use when creating, regenerating, or validating native AutoCAD drawings from a
  DWT or existing DWG, especially when editable DWG and repeatable PDF or PNG
  review artifacts are required. Do not use for format conversion alone or when
  a non-AutoCAD deliverable satisfies the request.
license: MIT
metadata:
  author: 42euge
  version: "0.1.0"
---

# AutoCAD drawing workflow

Produce a native, editable AutoCAD drawing while protecting its source template
and retaining enough evidence to reproduce and review the result. Treat file
health, visual quality, and engineering correctness as separate claims.

## Establish the drawing contract

Before changing files, identify:

- the drawing's purpose and authoritative design inputs;
- the source DWT or DWG, its ownership, and whether it may be modified;
- the required drawing number, title, revision, units, sheet, plot settings,
  DWG version, and review formats;
- whether the result is conceptual, buildable, or release-controlled; and
- which local changes and external publication actions are authorized.

Locate a user-mentioned local template when practical. Do not silently replace
it with a generic border. If a missing choice would materially change the
drawing or its release meaning, stop for that choice; otherwise record a
conservative assumption in the drawing notes or build manifest.

## Protect and inspect the source

Hash the source template before generation and treat it as read-only. Create a
derived drawing rather than editing the template in place. Inspect the actual
template before positioning geometry or populating metadata:

- model and paper-space extents, layouts, viewports, units, and plot settings;
- title-block insertion points, attribute tags, duplicate aliases, and revision
  fields;
- layers, text styles, external references, fonts, legal text, and other content
  that must survive generation.

Keep project facts, template-specific mappings, and machine-local tool paths in
configuration or adapters rather than embedding them in reusable drawing logic.

## Preflight the complete path

Check the operating system, installed AutoCAD edition and version, available
headless engine, required GUI permissions, generator sources, PDF inspection and
rasterization tools, output directories, and expected template hash. Detect an
open or locked target drawing before building.

For a repeated or checked-in workflow, expose one project-local interface with
the equivalent of `preflight`, `build`, and `verify`. Keep AutoLISP, shell, GUI
automation, and converter commands behind that interface so callers cannot
accidentally skip template protection, audit parsing, or artifact verification.
Use a neutral component/net model when the same drawing logic must support more
than one design; keep template and platform behavior in separate adapters.

## Generate native geometry

Prefer AutoCAD's headless engine for deterministic creation, layer assignment,
title population, save, and `AUDIT`. Generate real AutoCAD entities on named
layers; an embedded image inside a DWG is not an editable drawing. Save to an
explicit DWG version and retain the console log.

Require the configured `AUDIT` result—normally zero errors, fixes, and erased
objects—before accepting the build. A successful audit proves structural file
health only; it does not prove correct connectivity, dimensions, safety, or
design intent.

When working with AutoCAD for macOS or when headless PDF plotting fails, read
[references/macos-autocad-automation.md](references/macos-autocad-automation.md).
Keep any unavoidable GUI adapter narrow rather than moving generation and audit
into a fragile UI sequence.

## Export and review

Create the requested review formats from the audited DWG. Assert the selected
plotter, paper size, orientation, plot area, scale, and plot style rather than
accepting remembered GUI state. Close only the exact derived document and
discard export-only document changes when appropriate.

Rasterize the PDF and inspect it after every meaningful geometry, title-block,
font, or plot change. Check at least:

- borders, viewports, title and revision text, legal text, and page bounds;
- line weights, colors, font substitutions, wrapping, clipping, and overlaps;
- layer separation, labels, arrowheads, connection endpoints, and note
  readability; and
- whether the visual hierarchy matches the drawing's stated purpose.

Do not infer a clean visual result from a successful command or a clean audit.

## Verify and retain provenance

Fail the build if the source-template hash changed. Verify the native DWG type
and requested version, PDF page count and physical size, raster dimensions, and
absence of drawing locks or stale application state. Record a machine-readable
manifest containing the relevant input and adapter hashes, tool versions, audit
result, output hashes, and validation checks.

`verify` must reject outputs when an input, generator, adapter, or artifact has
changed since the last passing build. Preserve the last passing manifest when a
rebuild fails, and keep failure logs or screenshots that explain the failed
stage.

## Assess correctness and deliver

Review drawing semantics separately from artifact integrity. Trace important
connections, directions, dimensions, identifiers, and cross-document references
against the authoritative design inputs. Surface unresolved electrical,
mechanical, safety, thermal, EMC, or release decisions as explicit human gates.

Deliver the editable DWG, review artifacts, regeneration entrypoint, manifest,
and a concise validation summary. State what was and was not proven. Committing,
pushing, or opening a merge request requires the same explicit authorization as
any other repository workflow.
