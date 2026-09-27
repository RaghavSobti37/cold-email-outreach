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
| `referral` | People who reply and point to someone else | all | Highest reply rate. Always log them. |

## What works (from the first run, 27 Sep 2026)
- About 1 in 3 company homepages shows a usable email. Many sites only have a contact form, so skip those.
- A careers or freelancer address (jobs@, careers@, cv@, apply@, freelancers@) beats hello@ or info@.
- A published address can still be dead (Pocket Aces `freelancers@` bounced with 550). The bounce sweep catches these
  and puts them on the do-not-contact list automatically.

## Never
- Guessed patterns (firstname.lastname@), purchased lists, or scraped personal addresses from LinkedIn or Instagram.
- People who've asked not to be contacted, and anyone on the do-not-contact list.
