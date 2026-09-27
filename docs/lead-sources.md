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

## Never
- Guessed patterns (firstname.lastname@), purchased lists, or scraped personal addresses from LinkedIn or Instagram.
- People who've asked not to be contacted, and anyone on the do-not-contact list.
