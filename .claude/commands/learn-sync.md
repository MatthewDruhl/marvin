# /learn-sync - Sync Learning Tracker

Sync new topics from `~/Code/Learning/topics-learned.md` into `state/learning.md`.

## Instructions

### 1. Read Both Files
- `~/Code/Learning/topics-learned.md` - Source of truth for learned topics
- `state/learning.md` - MARVIN's spaced repetition tracker

### 2. Compare and Identify New Topics
For each section in `topics-learned.md`, check if the topic already exists in `state/learning.md`.

**Confidence mapping for new topics:**
- `Issues Needing More Guidance` items → **1/5** (lowest)
- `Topics Covered` and `Key Concepts Practiced` items → **2/5**

### 3. Add New Topics
For any topics NOT already in `state/learning.md`:
- Add to the appropriate section (Python Topics, matching the source section)
- Set confidence per mapping above
- Set Questions to `0/10`
- Set Last Reviewed to `—`
- Set Next Review to today's date
- Set Interval to `1 day`
- Set Status to `New`

### 4. Report Results
Show a summary:
- How many new topics were added (and list them)
- How many topics were already tracked (skip listing unless asked)
- If nothing new: "All topics already synced."
