# Lead sources

Where the system looks for contacts. Every lead records its `source_type` and `source_url`, so the Sources tab in the
sheet shows which sources produce replies and which produce bounces. Move effort toward the ones that work.

| source_type | Where | Tracks | Notes |
|---|---|---|---|
| `hn_whos_hiring` | Hacker News "Ask HN: Who is hiring?" (1st weekday of each month). Algolia API: `hn.algolia.com/api/v1/items/<id>` | tech_remote, creative_tech, editing_remote | Emails are posted by the hiring person, so bounce rates are very low. Filter for REMOTE plus worldwide/India; skip "US only". |
| `company_website` / `company_careers_page` / `company_contact_page` | The company's own site | all | Best-quality source. Only use addresses shown on the page. |
| `directory_designrush` | designrush.com agency lists (e.g. video production, Mumbai) | video_india, creative_tech | Gives company names and sites. Get the email from the company site, not the directory. |
| `github_awesome_creative_technology` | github.com/j0hnm4r5/awesome-creative-technology | creative_tech | 150+ experiential and interactive studios worldwide. |
| `clutch_directory` | clutch.co/in/agencies/video-production/... | video_india | Same approach as DesignRush. |
| `industry_article` | e.g. Homegrown's lists of indie labels, "top production houses" articles | video_india | Company names only; verify on their sites. |
| `creativedevjobs` | creativedevjobs.com | creative_tech | Job posts; apply links, with emails only sometimes. |
| `govt_directory_indiacinehub` | indiacinehub.gov.in/pscs-line-producers (Govt of India list of production service companies & line producers; paginated `?page=N`) | video_india | Line producers hire local DOPs, camera ops and editors for international shoots. Very relevant. 3 of 21 bounced, so the list is partly stale. |
| `referral` | People who reply and point to someone else | all | Highest reply rate. Always log them. |

## What works (from the first run, 27 Sep 2026)
- About 1 in 3 company homepages shows a usable email. Many sites only have a contact form, so skip those.
- A careers or freelancer address (jobs@, careers@, cv@, apply@, freelancers@) beats hello@ or info@.
- A published address can still be dead (Pocket Aces `freelancers@` bounced with 550). The bounce sweep catches these
  and puts them on the do-not-contact list automatically.

## Run 2 learnings (27 Sep 2026, evening)
- **Older HN threads (Oct 2025 – May 2026)** still produced about 23 relevant remote leads. Hiring managers read these inboxes long after posting. Say "if the role is still open".
- **India Cine Hub** gave 21 line-producer contacts in 3 fetches, the best yield per fetch so far.
- **Tooling note:** web fetch only runs without approval on URLs that came from a web-search result. Domains copied out of a directory page can get blocked, so search `"<company> <city> contact"` first and fetch the result URL.
- Bounce rate so far: 4 / 107 (3.7%), all from addresses that were published but dead.

## Run 3 learnings (28 Sep 2026): follow the replies
- **Who replied after day 1:** creative-development / WebGL studios (14islands wrote back personally; Makemepulse, Reckon
  Digital auto-acknowledged) and adventure / expedition film (Higher Earth asked about an Ecuador shoot). Indian agencies
  mostly stayed quiet or declined (Verve Media: "no openings").
- So run 3 went niche-first: 99 creative-dev / immersive / motion studios (EU, Americas, APAC), 45 travel/adventure crews
  and fixers (Iceland, Norway, Nepal, Bhutan, Mongolia, Morocco, Jordan, Kenya, Rockies, UK wildlife), 33 Indian
  travel/doc/line-production houses, 11 remote HN roles. New track: `adventure_video`.
- **Speed:** four research agents in parallel (one per niche), each writing its own `leads3_<niche>.json`, then four
  parallel senders. 188 sends in ~5 minutes; research is the slow part (~30 min).
- Good creative-studio sources: awesome-creative-technology, Psychoactive's "best WebGL agencies" post, Awwwards studio
  pages, then each studio's contact/careers page. Good adventure sources: "film fixer <country>" searches.
- Bounces: 3 / 188 (1.6%). One was an obfuscated `name[ATSIGN]domain` address (skip those next time), one a Google Group
  that doesn't accept outside mail, one a dead jobs@.
- Studio `jobs@` inboxes often auto-acknowledge (MLF, Tendril): that confirms delivery, but it isn't a reply.

## Run 4 learnings (28 Sep 2026, afternoon): coding track + link-rich emails
- Emails now go out as HTML with a plain-text twin: project names link to the live builds, and every email ends with
  labelled links (portfolio, coding portfolio bluepolaroid.com/coding, GitHub, LinkedIn, resume).
- New `coding_freelance` track: 79 web design / Webflow / Framer / Sanity / Shopify agencies (UK, IE, NL, DE, Nordics,
  ES, AU, NZ, CA, US, JP, SG, UAE) pitched for freelance / white-label Next.js builds, plus 25 remote dev roles
  (`tech_remote`) from careers pages and hnhiring.com. HN Jun–Sep 2026 posts with emails had all been emailed already.
- Morning-batch replies within 3 hours: Mudskipper (interested, team copied), Storytailors / Fixer Bhutan (interested),
  Camera Crew Germany and Cine Dreams (positive), Momkai, Dot Films, Lab212 (polite no). Adventure + natural-history
  video and creative studios keep answering.
- WebFetch can hit a per-session limit in subagents; relaunching later worked. Fallback is the browser pane, but every
  new site needs approval, so it's not practical for bulk research.

## Run 5 learnings (28 Sep 2026, night)
- 109 sent (61 crews/fixers worldwide, 23 coding agencies, 16 India wildlife/doc, 9 film+code studios), 1 bounce.
- **Evil Martians complained**: their `obey-frontend@` inbox belongs to a job post with its own application steps.
  Rule: never cold-email role-specific job inboxes; list them for Raghav to apply by hand.
- Web search is capped at ~200 per session, shared by all agents. Plan ~40 searches per agent and start from candidate
  lists saved from earlier runs.
- Communities: see `docs/communities.json` (36 entries). Best: Indian Media Jobs (Telegram, public preview with
  recruiter emails), Remote Front-End Jobs (Telegram), Framer Discord + Experts directory, Creative Paradise and Motion
  Freelance Club (Discord), AIO Cine (India crew marketplace), Reactiflux.

## Never
- Guessed patterns (firstname.lastname@), purchased lists, or scraped personal addresses from LinkedIn or Instagram.
- People who've asked not to be contacted, and anyone on the do-not-contact list.
