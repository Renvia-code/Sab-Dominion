# Interview science for the delivery page (R4)

*Agent R · 2026-11-01 08:57 · for the brief's "Delivery, backed by research" page and the rehearsal plan.*

How this was checked:
- Every DOI was resolved in Crossref, and title, journal, volume and pages were checked.
- Findings are quoted from the abstract, read in OpenAlex, Semantic Scholar or the authors' preprint.
- Raw responses are in `work/research_raw/lit_meta/`; the script is `work/scripts/r_lit_lookup.py`.
- Nothing here rests on a paper we could not read. Where only the metadata was reachable, the paper is listed as
  *not relied on*.

Strength labels:
- **Strong**: a meta-analysis or large review
- **Moderate**: several studies or one large one
- **Single**: one paper
- **Mixed**: replications disagree
- **Failed**: a replication found nothing

---

## The delivery page in one table (for B)

| Tip on the delivery page | Rests on | Strength | One practical rule |
|---|---|---|---|
| **The first minutes count** | Barrick, Swider & Stewart 2010; Swider et al. 2011 | Single (field study) + single | Open with a crisp, factual 30-second answer. Early competence judgments carry into the final score. |
| **Sell with facts; never embellish** | Swider et al. 2011; Barrick et al. 2009 | Single + strong (meta-analysis) | Self-promotion with real evidence helps. Image creation (stretching the truth) lowers end-of-interview scores. |
| **Expect structured, past-behaviour questions** | Sackett et al. 2022; McDaniel et al. 1994; Taylor & Small 2002 | Strong | Prepare 5–6 specific STAR stories mapped to the posting. Panels score answers against the same questions for everyone. |
| **State limits, then answer them** | O'Keefe 1999 | Strong (meta-analysis) | Name the weakness *and* the rebuttal. "Ten points is thin, so the headline uses thousands of county-days" beats hiding it, and beats naming it without an answer. |
| **Ask good questions, and follow up** | Huang et al. 2017 | Moderate (3 studies, live conversations) | Ask follow-up questions on what a panelist just said, not only prepared ones. |
| **Name the nerves "excitement"** | Brooks 2014; Bosshard & Gomez 2024; Ganley et al. 2021 | **Mixed: small effect** | Say "I'm excited" rather than "calm down". It is cheap and low-risk, but the pooled effect is small (d ≈ 0.2) and one math replication found nothing. Present it as a small edge, not a fix. |
| **Anxiety costs points, so rehearse** | Powell, Stanley & Brown 2018; McCarthy & Goffin 2004 | Strong (meta-analysis) + single | Anxiety and interview scores correlate at r = −.19. Rehearse out loud with a mock panel; familiarity lowers anxiety [I]. |
| **Charts: position beats angle and area** | Cleveland & McGill 1984; Heer & Bostock 2010 | Strong (classic, re-run by crowdsourcing) | Use bars, dots and lines on a common scale. Avoid pies and area for anything the panel must compare. |
| **Panels** | Dixon et al. 2002; McDaniel et al. 1994 | Review (mixed findings) | Each panelist may rate you separately. Answer the asker first, then bring in the others [I]. Give complete answers even when a point repeats. |
| **Answer first, then the support** | *No study verified* (the brief's practitioner lead, Minto, was not opened) | Practitioner | Keep it, labelled as common practice, without a citation. |
| **"I don't know" → "here's how I'd find out"** | *No study verified* | Practitioner | Keep it as advice; no citation. |
| **Pacing, the close, the follow-up note** | *No study verified* | Practitioner | Keep it as advice; no citation. |
| **Power posing** | Ranehill et al. 2015 | **Failed** | **Leave out.** |

---

## 1. Structured interviews: what the panel is likely doing

**Schmidt & Hunter (1998)**, *Psychological Bulletin* 124(2), 262–274. doi:10.1037/0033-2909.124.2.262
- **Found:** across 85 years of research, "GMA plus a structured interview (mean validity of .63)" is among the
  three best-predicting combinations.
- **Strength:** strong (meta-analytic summary). Later work revises the numbers down (Sackett et al. 2022).

**Sackett, Zhang, Berry & Lievens (2022)**, *Journal of Applied Psychology* 107(11), 2040–2068.
doi:10.1037/apl0000994
- **Found:** earlier validities were overcorrected and are "reduced by .10-.20 points". "Structured interviews
  emerged as the top-ranked selection procedure."
- **Strength:** strong. **Rule:** treat every question as scored. A panel using a structure compares answers
  question by question.

**McDaniel, Whetzel, Schmidt & Maurer (1994)**, *Journal of Applied Psychology* 79(4), 599–616.
doi:10.1037/0021-9010.79.4.599
- **Data:** 245 coefficients, 86,311 people.
- **Found:** validity depends on content, on "structured vs. unstructured; board vs. individual" and on the
  criterion. "Structured interviews were found to have higher validity than unstructured interviews."
- **Strength:** strong.

**Levashina, Hartwell, Morgeson & Campion (2014)**, *Personnel Psychology* 67(1), 241–293. doi:10.1111/peps.12052
- **Covers:** a narrative and quantitative review covering structure, impression management in structured
  interviews, situational vs past-behaviour questions, rating scales and probing.
- **Strength:** strong (review). It frames the topics; the directional findings below come from the meta-analyses.

## 2. Past-behaviour (STAR) vs situational questions

**Taylor & Small (2002)**, *Journal of Occupational and Organizational Psychology* 75(3), 277–294.
doi:10.1348/096317902320369712
- **Found:** "studies using past behaviour questions, when used with descriptively anchored answer rating scales,
  yielded a substantially higher mean validity estimate than studies using the situational question format ...
  (.63 versus .47)". Inter-rater reliabilities were similar (.79 and .77) with anchored scales.
- **Strength:** strong (meta-analysis).
- **Rule:**
  - Expect "Tell me about a time…". This matches the Dominion reports (R-068: "behavioral questions").
  - Each STAR story needs a specific situation, *your* action and a result. The resume supplies results; `[you: …]`
    where it doesn't.
- *Note:* McDaniel et al. (1994) found situational interviews more valid than "job-related" ones. That is a
  different comparison, so there is no contradiction.

## 3. The first minutes, rapport and impression management

**Barrick, Swider & Stewart (2010)**, *Journal of Applied Psychology* 95(6), 1163–1172. doi:10.1037/a0019918
- **Found:** "Candidates making better initial impressions received more internship offers (r = .22) and higher
  interviewer ratings (r = .42)." Initial impressions "may be based on useful judgments of candidate competence that
  occur in the opening minutes of the structured interview". The effect held even for a separate interviewer.
- **Strength:** single field study, structured interviews.
- **Rule:** the opening, meaning rapport talk plus the 30-second "tell me about yourself", is scored in practice.
  Make it about competence, not small talk.

**Swider, Barrick, Harris & Stoverink (2011)**, *Journal of Applied Psychology* 96(6), 1275–1288.
doi:10.1037/a0024005
- **Found:** "self-promotion was found to have a positive relationship (r = .20) and slight (r = -.11) and extensive
  (r = -.19) image creation were found to have negative relationships with end-of-interview scores", moderated by
  how the rapport-building stage went.
- **Strength:** single study.
- **Rule:** promote real results (the resume's numbers). Never stretch them. Embellishment is both wrong and,
  here, measurably counter-productive.

**Barrick, Shaffer & DeGrassi (2009)**, *Journal of Applied Psychology* 94(6), 1394–1411. doi:10.1037/a0016532
- **Found:** a meta-analysis of appearance, impression management and verbal and nonverbal behaviour. "What you see
  in the interview may not be what you get on the job and ... the unstructured interview is particularly impacted
  by these self-presentation tactics."
- **Strength:** strong. **Rule:** polish matters less in a structured panel than substance; prepare evidence first.

## 4. Interview anxiety and reappraisal (replication status included)

**Powell, Stanley & Brown (2018)**, *Canadian Journal of Behavioural Science* 50(4), 195–207. doi:10.1037/cbs0000108
- **Found:** "The overall meta-analytic correlation of −.19", moderated by measurement approach and interview type
  (mock vs real).
- **Strength:** strong (meta-analysis).

**McCarthy & Goffin (2004)**, *Personnel Psychology* 57(3), 607–637. doi:10.1111/j.1744-6570.2004.00002.x
- **Found:** a five-part interview-anxiety measure (Communication, Appearance, Social, Performance, Behavioral). "A
  multiple correlation of .34 was found for the 5 MASI scales in the prediction of interview performance."
- **Strength:** single (scale development, field sample).
- **Rule:** anxiety has several sources. Rehearse the *communication* part (the talk track) out loud; that is the
  part rehearsal can fix [I].

**Brooks (2014)**, *Journal of Experimental Psychology: General* 143(3), 1144–1158. doi:10.1037/a0035325 (original)
- **Found:** "individuals who reappraise their anxious arousal as excitement feel more excited and perform better",
  using "minimal strategies such as self-talk (e.g., saying 'I am excited' out loud)". The tasks were karaoke,
  public speaking and maths.

**Replication status** (as of 1 Nov 2026, from what we could open):
- **Ganley et al. (2021)**, *Journal of Numerical Cognition* 7(1), 4–19. doi:10.5964/jnc.6065
  - 300 students; one of the arms was "reappraisal as excitement".
  - "none of the interventions had an effect on reports of state anxiety or performance on a difficult math
    assessment"; the authors say the findings "were not consistent with results of previous work".
  - A **non-replication** for maths tests.
- **Bosshard & Gomez (2024)**, *Scientific Reports* 14. doi:10.1038/s41598-024-58408-w
  - A meta-analysis of randomised trials of stress-arousal reappraisal (a broader family that includes the
    excitement framing): 44 effect sizes, "an overall small significant improvement in task performance (d = 0.23)".
  - Reappraisal-only arms: d = 0.22. Effects were larger for public-performance tasks (d = 0.34) than for written
    cognitive tasks (d = 0.20).
  - The authors: "not 'silver bullets'".
- **A preregistered direct replication of Brooks's public-speaking study** (OSF registration cyzgj, 22 Nov 2019,
  https://osf.io/cyzgj) lists no data or paper. **No result is available.**
- **Related:** Jamieson et al. (2010), *Journal of Experimental Social Psychology* 46(1), 208–212
  (doi:10.1016/j.jesp.2009.08.015), found arousal reappraisal improved practice and real GRE math scores. The review
  by Jamieson, Mendes & Nock (2013), *Current Directions in Psychological Science* 22(1), 51–56
  (doi:10.1177/0963721412461500), summarises the approach.

**Verdict:** **mixed, small.** B may include "say 'I'm excited'" as a low-cost tip, worded as a small edge with
mixed replication. It must not be presented as a proven fix.

## 5. Asking questions

**Huang, Yeomans, Brooks, Minson & Gino (2017)**, *Journal of Personality and Social Psychology* 113(3), 430–452.
doi:10.1037/pspi0000097
- **Found:** "people who ask more questions, particularly follow-up questions, are better liked by their
  conversation partners"; the effect runs through perceived responsiveness ("listening, understanding, validation,
  and care").
- **Strength:** moderate (3 studies of live conversations and speed-dating). Interviews are inferred, not tested
  [I].
- **Rule:** at "Do you have questions for us?", ask one follow-up on something a panelist said. Use the prepared
  questions (A1–A8 in `top40.md`) after that.

## 6. Stating limits: two-sided messages

**O'Keefe (1999)**, *Annals of the International Communication Association* (Communication Yearbook) 22(1),
209–249. doi:10.1080/23808985.1999.11678963
- **Found:** "refutational two-sided messages on nonadvertising topics enjoy significantly greater credibility and
  persuasiveness". "Nonrefutational two-sided messages on nonadvertising topics are not significantly different in
  credibility and are significantly less persuasive."
- **Strength:** strong (random-effects meta-analysis).
- **Rule:** stating a limit only helps when you answer it in the same breath. This is exactly the deck's pattern:
  - "r = 0.70 on ten points is thin → the headline uses county-days"
  - "the DOM zone includes other utilities → that's why I don't attribute it"
  - "public data can't pick the circuit → here's the data I'd ask for"

*Eisend (2006)*, *International Journal of Research in Marketing* 23(2), 187–198. doi:10.1016/j.ijresmar.2005.11.001.
The metadata is verified but the abstract was not reachable (publisher), so it is **not relied on**. It concerns
advertising, which O'Keefe treats separately.

## 7. Panel interviews

**Dixon, Wang, Calvin, Dineen & Tomlinson (2002)**, *Public Personnel Management* 31(3), 397–428.
doi:10.1177/009102600203100310
- **Found:** "the panel interview remains an important yet controversial tool". Reviews "have yielded conflicting
  results concerning its reliability and predictive validity". The quality of a panel depends on its setting,
  structure, scoring anchors, question type, training and how ratings are combined.
- **Strength:** review; findings mixed. McDaniel et al. (1994) list "board vs. individual" as a moderator of
  validity, without a simple direction in the abstract.
- **Rules [I]:**
  - Three panelists may score separately and then combine, so every answer must stand on its own.
  - Answer the person who asked, then include the others.
  - Expect the panel's roles to differ (manager, analyst, partner team). The research gives no specific rule here.

## 8. Graphical perception (for the deck)

**Cleveland & McGill (1984)**, *Journal of the American Statistical Association* 79(387), 531–554.
doi:10.1080/01621459.1984.10478080
- **Found:** people decode some encodings more accurately than others. "Graphs should employ elementary tasks as
  high in the ordering as possible." The authors recommend "dot charts, dot charts with grouping, and
  framed-rectangle charts" over pie and divided-bar charts.
- **Strength:** strong (a classic; experimental).

**Heer & Bostock (2010)**, CHI 2010, 203–212. doi:10.1145/1753326.1753357
- **Found:** "We replicate previous studies of spatial encoding and luminance contrast". "Crowdsourced perception
  experiments are viable."
- **Strength:** moderate. [I] The earlier ranking held up when re-run; the abstract does not spell this out.
- **Rule:**
  - Compare values by position on a shared axis (bars, dots, lines).
  - Never ask the panel to compare angles or areas.
  - The deck's 24-hour profile and SAIFI/CAIDI split already follow this.

## 9. Leave out

**Power posing.** Ranehill et al. (2015), *Psychological Science* 26(5), 653–656. doi:10.1177/0956797614553946
- Title: "Assessing the Robustness of Power Posing: No Effect on Hormones and Risk Tolerance in a Large Sample of
  Men and Women".
- Semantic Scholar's summary: the study "found no significant effect of power posing on hormonal levels or in any
  of the three behavioral tasks".
- **Failed replication; do not use.**

**Practitioner-only tips** (answer-first, "here's how I'd find out", pacing, the close, the thank-you note) have no
study verified in this run. Keep them as advice without a citation.

**Huffcutt, Van Iddekinge & Roth (2011)**, *Human Resource Management Review*. doi:10.1016/j.hrmr.2011.05.003. The
metadata is verified but the abstract was not reachable, so it is **not relied on**.

## Sources

All accessed 2026-11-01. DOIs resolved in Crossref; abstracts read as noted.

| Short cite | DOI | Abstract read via |
|---|---|---|
| Schmidt & Hunter 1998 | 10.1037/0033-2909.124.2.262 | OpenAlex |
| Sackett et al. 2022 | 10.1037/apl0000994 | OpenAlex |
| McDaniel et al. 1994 | 10.1037/0021-9010.79.4.599 | OpenAlex |
| Levashina et al. 2014 | 10.1111/peps.12052 | OpenAlex |
| Taylor & Small 2002 | 10.1348/096317902320369712 | OpenAlex |
| Barrick, Swider & Stewart 2010 | 10.1037/a0019918 | OpenAlex |
| Swider et al. 2011 | 10.1037/a0024005 | OpenAlex |
| Barrick, Shaffer & DeGrassi 2009 | 10.1037/a0016532 | OpenAlex |
| Powell, Stanley & Brown 2018 | 10.1037/cbs0000108 | Semantic Scholar |
| McCarthy & Goffin 2004 | 10.1111/j.1744-6570.2004.00002.x | OpenAlex |
| Brooks 2014 | 10.1037/a0035325 | OpenAlex |
| Ganley et al. 2021 | 10.5964/jnc.6065 | OpenAlex |
| Bosshard & Gomez 2024 | 10.1038/s41598-024-58408-w | OpenAlex |
| Jamieson et al. 2010 | 10.1016/j.jesp.2009.08.015 | Semantic Scholar |
| Jamieson, Mendes & Nock 2013 | 10.1177/0963721412461500 | OpenAlex |
| OSF replication registration | https://osf.io/cyzgj (API record) | OSF API: no data, no paper |
| Huang et al. 2017 | 10.1037/pspi0000097 | OpenAlex |
| O'Keefe 1999 | 10.1080/23808985.1999.11678963 | OpenAlex |
| Eisend 2006 | 10.1016/j.ijresmar.2005.11.001 | not reachable: not relied on |
| Dixon et al. 2002 | 10.1177/009102600203100310 | OpenAlex |
| Cleveland & McGill 1984 | 10.1080/01621459.1984.10478080 | OpenAlex |
| Heer & Bostock 2010 | 10.1145/1753326.1753357 | OpenAlex |
| Ranehill et al. 2015 | 10.1177/0956797614553946 | Semantic Scholar TLDR + title |
| Huffcutt et al. 2011 | 10.1016/j.hrmr.2011.05.003 | not reachable: not relied on |
