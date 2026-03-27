"""Curated source content for the static shalyt.com website."""

# SITE_TITLE stores the public website title displayed in the shared header.
SITE_TITLE = "Michael Shalyt"

# SITE_DESCRIPTION stores the short tagline reused in metadata and navigation chrome.
SITE_DESCRIPTION = "Thinker, Hacker, Maker."

# PAGE_DATA stores the page order, routes, and HTML bodies for the published site.
PAGE_DATA = [
    {
        "title": 'Home',
        "slug": 'home',
        "order": 1,
        "body_html": r"""
<div class="home-hero">
<img class="home-hero-banner" src="/media/Banner_Window.jpg" alt="Michael Shalyt portrait banner." />
</div>

<div class="wp-block-group">
<div class="wp-block-group">
<p><strong>Welcome!</strong></p>

<p><strong>You've reached my spot on the web. It was created as a sort of online portfolio to show stuff I'm proud of but don't always fit into my normal CV (that's below).</strong></p>

<p><strong>Please see some of my work in <a href="/ai/">AI</a>, <a href="/cyber-security/">Cyber Security</a>, <a href="/physics/">Physics</a>, <a href="/games/">Games</a> and <a href="/ideas-2/">other topics</a>.</strong></p>

<p><strong>For expert consulting or collaborations - feel free to contact me: michael(at)shalyt.com or via any social media.</strong></p>
</div>
</div>

<div class="pdf-embed"><iframe src="/media/MichaelShalyt_2025_anon.pdf#toolbar=0&navpanes=0&view=FitH" title="Michael Shalyt CV PDF"></iframe></div>

""",
    },
    {
        "title": 'AI',
        "slug": 'ai',
        "order": 2,
        "body_html": r"""
<h2><strong><span style="text-decoration: underline;">Ramanujan Machine</span></strong></h2>

<p>Since 2023 I lead the <a href="https://www.ramanujanmachine.com/">Ramanujan Machine Group</a> at the Technion under Prof. Ido Kaminer, working on the intersection of AI and mathematics. The field is changing very quickly - AI models, symbolic tools (both external and <a href="https://github.com/RamanujanMachine/">our own libraries</a>), vibe coding - and we apply it to explore mathematical spaces and <a href="https://www.pnas.org/doi/10.1073/pnas.2321440121">algorithmically discover</a> new formulas and conjectures.</p>

I like to describe our work as "doing math like engineers", automating ingenuity.</p>

<p>Our recent projects include the "ASyMOB" benchmark for algebraic symbolic reasoning (<a href="https://www.ramanujanmachine.com/asymob-algebraic-symbolic-mathematical-operations-benchmark/">blogpost</a>, <a href="https://arxiv.org/abs/2505.23851">paper</a>), "From Euler to AI" (<a href="https://www.ramanujanmachine.com/results/from-euler-to-ai-unifying-formulas-for-mathematical-constants/">blogpost</a>, <a href="https://neurips.cc/virtual/2025/loc/san-diego/poster/117099">paper</a>) - unifying hundreds of formulas for Pi throughout the centuries into a single Conservative Matrix Field (see video below), and <a href="https://neurips.cc/virtual/2024/poster/95491">"Unsupervised Discovery of Formulas for Mathematical Constants"</a> - using dynamic convergence behavior to cluster 1.7 million unknown formulas and discover novel formulas for multiple mathematical constants - which we presented in Vancouver:

<figure class="wp-block-image"><img src="/media/neurips-2024-poster.jpg" alt="Presenting the NeurIPS 2024 poster." /><figcaption>NeurIPS 2024</figcaption></figure>

<div style="text-align:center;">
<div class="video-embed"><iframe src="https://www.youtube-nocookie.com/embed/Uk04gfIt8yM" title="Conservative matrix fields talk" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>
</div>

<p class="video-caption">Created for the 3Blue1Brown "Summer of Math Exposition", where we reached the final round.</p>


<h2><strong><span style="text-decoration: underline;">Evo.Do</span></strong></h2>

<p>Mid 2018 I left my role as CEO of Aperio Systems to start a new company: Evo.Do. We built autonomous AI-bots that tested and validated games, based on Reinforcement Learning algorithms.&nbsp;</p>

<p>It’s hard to make sure that a complicated game or app works properly after every change, patch, design shift etc. It takes thousands of tests and weeks of tester-time to do a full validation. For many years developers tried automating the process via scripting - programming a set of actions that should take the app from state A to state B and validate that indeed we reached state B. Unfortunately scripted tests are very “brittle” - any small change can make the test fail (not reach the intended end goal), even if there was no bug introduced. Devs ended up spending more time maintaining and fixing tests than fixing the actual game, and most went back to manual testing.</p>

<p>Evo strived to combine the best of both worlds: the speed and accuracy of test scripts with the adaptivity and flexibility of human testers. The user defines the goal of the test (for example “make sure the key can be picked up”) and the bot learns on its own (through trial and error) how to achieve that goal:</p>

<div style="text-align:center;"> 
<div class="video-embed"><iframe src="https://www.youtube-nocookie.com/embed/liHOaiCklQw" title="YouTube video" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>
</div>

<p>The novel approach (<a href="/media/EvoPatent_P-582424-USP-APP-18MAR19.pdf">patent pending</a>) garnered some interest and we were <a href="https://www.calcalist.co.il/articles/0,7340,L-3741689,00.html">accepted to the inaugural batch of Tel Aviv University backed Xccelerator</a> program, where I gave a pitch during the closing ceremony:</p>

<div style="text-align:center;"> 
<div class="video-embed"><iframe src="https://www.youtube-nocookie.com/embed/5yWcT4L0Bgo" title="YouTube video" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>
</div>

<p>And later got into the largest startup accelerator in the world: Y Combinator (AI cohort). </p>

<div class="wp-block-image"><figure class="aligncenter is-resized"><img src="https://lh4.googleusercontent.com/TDUEZCLtjJm0w9HSKEDrbFcLwO76sdZ5M1wmhntc-SAVJ9RwsOcdYXMZL8CtrYI9flWp2fWi_X_0topRKY9-WfyfmJu5BR5Ub9gnqdDC0GQSJb4G_W1dj_l3KDx1Fo1WzVc8wyKC" alt="" width="600" height="400"/></figure></div>

<p>Where I pitched at the famous YC demo day:</p>

<div style="text-align:center;"> 
<div class="video-embed"><iframe src="https://www.youtube-nocookie.com/embed/HzEG2J-ev_8" title="YouTube video" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>
</div>

<p>Going through YC was a life-goal of mine - so I got to strike that off the list as completed :).</p>

""",
    },
    {
        "title": 'Cyber Security',
        "slug": 'cyber-security',
        "order": 3,
        "body_html": r"""
<h2><strong><span style="text-decoration: underline;">Aperio Systems</span></strong></h2>

<p><strong>I was a Co-Founder, CEO &amp; VP Product</strong> at Aperio (2016-2018). We created algorithms to validate physical sensor data in heavy manufacturing facilities – against data malfunctions and malicious tampering – using <em>signal processing and machine learning</em>. In that time we went from an idea to a deployed product, first customers and first millions of dollars raised. The company received multiple awards (notably <em>Gartner’s 2017 “cool vendor”</em> choice and CDM 2017 infosec award):</p>

<div class="wp-block-image"><figure class="aligncenter"><img src="/media/20171225_172602-scaled.jpg" alt="" class="wp-image-86"/></figure></div>

<div class="wp-block-image"><figure class="aligncenter size-medium"><img src="/media/19621108_10211726160862779_7361330908298307337_o.jpg" alt="" class="wp-image-85"/></figure></div>

<p>We won multiple competitions (like the <a href="https://www.timesofisrael.com/aperio-systems-wins-cybertech-startup-competition/">CyberTech Startup Competition</a> in Israel, <a href="https://bizplus.ie/aperio-wins-esb-pitch-off-competition/">ESB Pitch-off</a> in Ireland, Free Electrons in Singapore, etc.):</p>

<div style="text-align:center;"> 
<div class="video-embed"><iframe src="https://www.youtube-nocookie.com/embed/OLIY18_Bz7g" title="YouTube video" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>
</div>

<p>Some top-tier publications got interested in Aperio, and we were featured in outlets like<strong> <a href="https://www.forbes.com/sites/gilpress/2016/11/15/artificial-intelligence-lie-detector-to-protect-critical-infrastructure/">Forbes</a>, <a href="https://techcrunch.com/2018/02/07/aperio-raises-a-4-5m-seed-round-to-protect-power-plants-from-hackers/">Techcrunch</a>, <a href="https://www.bloomberg.com/news/articles/2016-11-15/israeli-tech-last-line-of-defense-for-power-plant-cyber-attacks">Bloomberg</a>, <a href="https://www.cnbc.com/2017/05/17/the-nsa-is-still-the-best-says-israeli-cybersecurity-chief.html">CNBC</a> </strong>and many others.</p>

<p>I've represented Aperio at various conferences focused both on information security and heavy manufacturing digitization:</p>

<div class="wp-block-image is-style-default"><figure class="aligncenter size-medium"><img src="/media/20180515_160643_cut-scaled.jpg" alt="" class="wp-image-88"/></figure></div>

<p>And gave talks at many of them. For example RSA in San Francisco:</p>

<div style="text-align:center;">
<div class="video-embed"><iframe src="https://www.youtube-nocookie.com/embed/d3DhWbM9uak" title="YouTube video" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>
</div>

<h2><strong><span style="text-decoration: underline;">Check Point Software Technologies</span></strong></h2>

<p>Once I finished my army service, the first job I chose was as a malware research team leader at Check Point (2014-2015). I managed 8 researchers (2 abroad) working on PC and Android malware analysis, reverse engineering and machine-learning-for-cyber. Below is some of the work we made public.</p>

<h4><strong><span style="text-decoration: underline;">Man In The Binder</span></strong></h4>

<p>In February 2015 I’ve attended the<a href="https://sas.kaspersky.com/"> Kaspersky SAS</a> invite-only information security conference as a speaker. I’ve presented a research conducted in my team at Check Point – describing a fundamental part of Android’s architecture (the Binder) and it’s potential dangers. This is the technical basis for the “Spy In Your Pocket” talk below. </p>

<div style="text-align:center;"> 
<div class="video-embed"><iframe src="https://www.youtube-nocookie.com/embed/YXVmlmuOxdw" title="YouTube video" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>
</div>

<h4><strong><span style="text-decoration: underline;">Spy In Your Pocket</span></strong></h4>

<p>I gave this lecture at the<a href="http://fst.net.au/speakers/michael-shalyt"> 7th Annual Technology &amp; Innovation – the Future of Security in Financial Services</a> in Melbourne and again in Sydney. The talk is an introduction to the Android malware landscape, explaining why (in my opinion) the Android operating system should be in the focus of any information security specialist today, showing a demonstration of an innovative data-theft technique we researched and offering some protection methods: </p>

<div style="text-align:center;"> 
<div class="video-embed"><iframe src="https://www.youtube-nocookie.com/embed/X8zKnH1QkhU" title="YouTube video" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>
</div>

<p>The slides can be found<a href="https://fst.net.au/sites/default/files/file/conferences/presentations/michael_shalyt-whitehat.pdf"> here</a>. A better quality audio recording (from Sydney – where I won the “best speaker” title) can be found<a href="https://fst.net.au/sites/default/files/file/conferences/audios/07._michael_shalyt.mp3"> here</a>. The content was transformed into an article and published:<a href="/media/SpyInYourPocket_FST_Media.pdf"> SpyInYourPocket_FSTMedia</a>. I gave an adapted version of this talk in Detroit (example of an<a href="https://store.checkpoint.com/events/invitationPage.htm;tenantID=events?method=enterInvitation&amp;eventCode=15-q2-fmkt-uscentral-sm-malware-detroit"> invitation</a>), Chicago, St Louis, Minneapolis and as a webinar.</p>

<h4><strong><span style="text-decoration: underline;">“Hacking the Hacker”</span></strong></h4>

<p>One of the problems we tackled in my team at Check Point was the rise of cryptoviruses, a certain category of ransomware that encrypts all your personal files once it infects the computer – then demands you pay ransom to the criminals in exchange for the decryption key. One such cryptovirus was Dircrypt. We reverse engineered the malware and found its encryption implementation to contain mistakes – mistakes which allowed us to save most of the personal data of a victim without paying any ransom. We published the findings on Check Point’s website (full article available <a href="https://www.checkpoint.com/download/public-files/TCC_WP_Hacking_The_Hacker.pdf">here</a>), and got some traction in the media (for example, <a href="http://tech.wp.pl/kat,1009779,title,Zhakowali-hakerow-Bedzie-mozna-odzyskac-zaszyfrowane-dane,wid,16919004,wiadomosc.html">here</a> and <a href="http://www.itnews.sk/spravy/bezpecnost/2014-09-29/c165236-vydieracsky-ransomware-dircrypt-sifrujuci-subory-bol-prelomeny">here</a>). We also gave a talk to the general Check Point audience – explaining the research story: </p>

<div class="slideshare-embed"><iframe src="https://www.slideshare.net/slideshow/embed_code/key/mk3qPT20ajXk0s" title="How and why we defeated the DirCrypt ransomware" loading="lazy" allowfullscreen></iframe></div>

<h4><strong><span style="text-decoration: underline;">“Volatile Ceder”</span></strong></h4>

<p>On the 31/3/15 we published our research describing “<a href="http://blog.checkpoint.com/2015/03/31/volatilecedar/">Volatile Cedar</a>” (<a href="https://www.checkpoint.com/downloads/volatile-cedar-technical-report.pdf">full report</a>) – a cyber espionage campaign operating at least since 2012 with Lebanese origins (<a href="http://www.haaretz.com/news/diplomacy-defense/.premium-1.650860">suspected to be run by the Hezbollah</a>). The disclosure generated a lot of media buzz – I was interviewed (among others)<a href="http://www.techworld.com/news/security/middle-eastern-volatile-cedar-cyberattack-breached-western-defence-firms-3606016/"> here</a>,<a href="http://www.techfromthenet.it/201504031235/News-analisi/cyberspionaggio-globale-intervistiamo-michael-shalyt-di-check-point.html"> here</a> and<a href="http://www.golem.de/news/operation-volatile-cedar-spionagesoftware-aus-dem-libanon-1503-113267.html"> here</a>.

</p>

""",
    },
    {
        "title": 'Physics',
        "slug": 'physics',
        "order": 4,
        "body_html": r"""
<h2><strong><span style="text-decoration: underline;">Control of a 2-Level System to Reduce Colored Noise</span></strong></h2>

<p>The main part of my MSc degree in Physics (quantum information) was the thesis. Its abstract can be found<a href="http://www.graduate.technion.ac.il/Theses/Abstracts.asp?Id=27973"> here</a> and the complete work can be downloaded:<a href="/media/Michael_Shalyt_Control-of-a-2-Level-System-to-Reduce-Colored-Noise.pdf"> Michael_Shalyt_Control of a 2-Level System to Reduce Colored Noise</a>.</p>

<p>This research was the seed for a wider approach – published in the New Journal of Physics:<a href="https://iopscience.iop.org/1367-2630/17/4/043009/"> https://iopscience.iop.org/1367-2630/17/4/043009/</a>. The article is freely available<a href="https://iopscience.iop.org/1367-2630/17/4/043009/pdf/1367-2630_17_4_043009.pdf"> here</a>. This particular journal encourages authors to create a video abstract of their work:</p>

<div style="text-align:center;"> 
<div class="video-embed"><iframe src="https://www.youtube-nocookie.com/embed/DgxrYuqKWco" title="YouTube video" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>
</div>

<h2><strong><span style="text-decoration: underline;">Photon-energy qubit generation by spontaneous emission in a V-type system</span></strong></h2>

<p>During my final year as an undergraduate (studying Electrical Engineering and Physics at the<a href="http://www.technion.ac.il/en/"> Technion</a>) I collaborated with 2 PhD students (in<a href="http://webee.technion.ac.il/labs/micro_photonics/"> Prof. Meir Orenstein’s group</a>, EE faculty) on a research project in quantum optics. The results were published in the Journal of Physics B (<a href="https://iopscience.iop.org/0953-4075/43/10/105502">link</a>). The full article:<a href="/media/Photon-energy-qubit-generation-by-spontaneous-emission-in-a-V-type-system.pdf"> Photon-energy qubit generation by spontaneous emission in a V-type system</a>.</p>

<p>In the pursuit of the quantum computation dream, scientists suggested various methods of implementing qubits (the bits of quantum computers). To this day there is no clear winner -  each mechanism has its pros and cons. We focused on energy-superposition qubits (think of the qubit as a photon being both “red” and “blue” simultaneously – how much is it “red” vs. how much “blue” is what encodes the information). The research dealt with the initialization problem - how to create energy qubits in arbitrary starting states with speed and precision.</p>

<h2><strong><span style="text-decoration: underline;">Physics Olympiad</span></strong></h2>

<p>After a rather grueling learning and training procedure throughout my final year in high school, I passed all the qualification exams and participated in the 36th IPHO (International Physics Olympiad) as part of the national team (and<a href="http://www.olimpas.lt/konspektai/36_tfo/final_marking_results_and_prizes.htm"> scored highest among Israelis</a>). </p>

<p>The whole process had a great influence on me.  Beyond the knowledge and skills - it taught me that with a lot of hard work I could achieve more than I previously considered possible. This influence, as well as the great people in the Olympiad community, convinced me to become a guide myself. I’ve been coaching the next generations of IPHO participants ever since, including at the 12th Asian Physics Olympiad (2011) and the <a href="https://www.ipho2019.org.il/">50th IPHO</a> (2019).</p>

<p>One of the ideas we had for improving the level of physics education in schools is a series of short lectures explaining fundamental physics principles in alternative ways. This is the pilot, talking about Galeleo’s gravity model:</p>

<div style="text-align:center;"> 
<div class="video-embed"><iframe src="https://www.youtube-nocookie.com/embed/SfegIgkQ6aY" title="YouTube video" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>
</div>

<h2><strong><span style="text-decoration: underline;">The time traveler’s loneliness</span></strong></h2>

<p>I love explaining complex ideas in simple terms, so I took a course during my fourth year at the Technion called “Science in the Media” - teaching methods to make scientific topics accessible without losing the core concepts. One of the projects assigned to us was to write a popular-science piece based on an interview – for a hypothetical newspaper. Mine was selected to be published in an actual newspaper (see<a href="http://www.ynet.co.il/articles/0,7340,L-3734046,00.html"> article</a>) and a<a href="http://www.hayadan.org.il/lonlyness-of-time-traveler-1508092"> popular science website</a>.</p>

<p>The article is about the investigation of closed time-loops (more commonly known as “time-machines”…) under the theoretical restrictions of General Relativity, based on an interview with Dr. Dana Levanony – then a PhD student studying the subject.</p>

""",
    },
    {
        "title": 'Games',
        "slug": 'games',
        "order": 5,
        "body_html": r"""
<h3><a href="http://fireside-tales.blogspot.com"><strong><span style="text-decoration: underline;">Fireside Tales</span></strong></a></h3>

<p>Fireside Tales is a collaborative storytelling card game for 4 to 8 players that<a href="http://www.natalycreates.com/"> Nataly Eliyahu</a> and I worked on as a side project for almost 1.5 years. The goal of the game is to tell an enjoyable story together by suggesting funny/crazy/surprising story elements represented by the cards you play. It underwent numerous design overhauls, detail variations and playtesting sessions – which not only made the game better but also taught us a lot about game design and teamwork. You can find more information about the game itself <a href="http://fireside-tales.blogspot.com">here</a> and read about it’s origins <a href="https://fireside-tales.blogspot.co.il/search/label/Design">here</a>.</p>

<p>We finally had a launch event for Fireside Tales at <a href="http://2015.iconfestival.org.il/">Icon 2015</a>. Here’s a video recorded after the end of the official event – I’m playing with some people who stayed for another game:</p>

<div style="text-align:center;">
<div class="video-embed"><iframe src="https://www.youtube-nocookie.com/embed/dYVocV03EL8" title="YouTube video" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>
</div>

<h3><strong><span style="text-decoration: underline;">Behavioral Economics</span></strong></h3>

<p>Back in 2012 I became interested in Behavioral Economics - specifically the acknowledgment that humans have feelings, emotions and habits that affect their judgment and decision making. It sounds obvious when it’s written like that but back when <a href="http://danariely.com/">Prof. Dan Ariely</a>’s book “Predictably Irrational” came out it was an instant best seller.&nbsp;</p>

<p>Behavioral Economics pushed me to think about crossovers between different fields of applied psychology - for example about the question “why do I like completing tasks in games but hate tasks in real life?”.&nbsp;</p>

<p>Through that pursuit I’ve created Alfred (together with <a href="https://www.linkedin.com/in/ravidgal/">Ravid</a>) - my own task management app that advises the user on what to do next and sets goals that adapt themselves based on your past progress and preferences (classic game design elements):</p>

<div class="wp-block-image"><figure class="aligncenter is-resized"><img src="https://lh4.googleusercontent.com/sW4uS0tOi6QIr-2qaGcXg7AF3B0KVo4EmAMVsU5mFrAAtpVKCvRlQg7MRkM18hZ2q83ZamP-HPxri7i5ifVoMyPQ0YuI27vl4hUG0jJGpUl2lZezd7-o6ypG6lonZuWtLwvfBW-P" alt="" width="225" height="384"/></figure></div>

<p>And was a “visiting scholar” under the lab of Dan Ariely - working with fintech startups in San Francisco to apply Behavioral Economics research results to real product design. This is a photo from the final dinner - with me trying to play it cool next to one of my role models :) </p>

<div class="wp-block-image"><figure class="aligncenter"><img src="https://lh6.googleusercontent.com/4bxjpBvPJQGtQrROfOJw-bicrE7La9XpQ864XPDYwcalA-Yca1jhiFc2MAPtntzLBgOkTSBY1EUsXCd2uo2VewhYRiAwuCeOyFeNbZa2QGQKaXl9JA3-vyx7I8nalU2dhmARsH1S" alt=""/></figure></div>

<h3><strong><span style="text-decoration: underline;">Game Economics</span></strong></h3>

<p>As part of my “let’s analyze everything!” mentality, when I’m really into a game I sometimes try to “reverse engineer” the game design, progression systems, player based economy etc. a couple of these “mini-research” projects were featured on Gamasutra (about <a href="https://www.gamasutra.com/blogs/MichaelShalyt/20170911/305342/Path_of_Exile_Economy_Currency_Trading.php">Path of Exile trading</a> and <a href="https://www.gamasutra.com/blogs/MichaelShalyt/20160418/270645/The_Math_Of_Clash_Royale.php">Clash Royale progression rate</a>). The later even landed me my first paid invited research job - analyzing Clash Royale unit balance (you can read about the <a href="/media/ClashRoyaleBalanceEquation.pdf">process</a> and the <a href="/media/ClashRoyaleBalanceEquation-Final.pdf">final summary</a>).&nbsp;</p>

<h3><a href="http://www.kongregate.com/games/MichaelShalyt/i-have-a-mouth-and-i-must-clean"><strong><span style="text-decoration: underline;">I Have A Mouth And I Must Clean (IHAM)</span></strong></a></h3>

<p>We made IHAM in 48 hours during the Global Game Jam 2016. In addition to the loads of fun we had building, playtesting and balancing this humoristic PVP game (depicting the epic struggle of germs vs. toothbrush) - there were quite a few lessons to be learned, as in any high intensity situation, so I wrote a <a href="http://lifeinagraph.shalyt.com/2016/02/yes-you-can-life-lessons-from-game-jam.html">post about it</a> that was later <a href="https://www.gamasutra.com/blogs/MichaelShalyt/20160217/265901/quotI_Have_a_Mouth_and_I_Must_Cleanquot__Postmortem.php">featured on Gamasutra</a>.</p>

<h3><strong><span style="text-decoration: underline;">Christmas Heist</span></strong></h3>

<p>Another Game Jam project - this time 36 hours and with a team distributed in 3 locations.&nbsp;</p>

<div class="wp-block-image"><figure class="aligncenter is-resized"><img src="https://lh3.googleusercontent.com/D7NtFcPvpjI73lOzQtFVeMWV62nBW1r5vYdJM7J2Icc2SjMHvOGMzQOJX5zqmoxiAcJxB9SAGrg2Yi2VJAi7jGctoa8h559_idgsKsMKUjwTi5rxNTGkeUsiHjxrnw0ylMe6JxZw" alt="" width="400" height="225"/></figure></div>

<p>You can play it here:<br><a href="https://ldjam.com/events/ludum-dare/40/christmas-heist">https://ldjam.com/events/ludum-dare/40/christmas-heist</a></p>

<h3><a href="http://unwrittencritten.shalyt.com/"><strong><span style="text-decoration: underline;">Unwritten? Critten!</span></strong></a></h3>

<p>This is a fun side project created from scratch by<a href="http://www.natalycreates.com/"> Nataly Eliyahu</a> and I in ~1.5 weeks. At the time we were considering various ways we could help aspiring and hobbyist writers to write more and better, a cute site that motivates you is<a href="http://writtenkitten.net/"> http://writtenkitten.net/</a> – showing you a picture of a cute kitten every set amount of words you write. We thought it would be funny to reverse the concept – and so <a href="http://unwrittencritten.shalyt.com/">Unwritten? Critten!</a> was born (try it for yourself).</p>

<h3><strong><span style="text-decoration: underline;">Table-top war machines</span></strong></h3>

<p>I always liked building toys/gadgets/mechanisms. One such mechanism – the table-top catapult – was cool enough for me to conduct catapult-construction workshops at 2 conventions (“Mahanet” and<a href="http://2014.iconfestival.org.il/"> Icon 2014</a>) and even <a href="https://www.facebook.com/photo.php?fbid=10203181024919721&amp;set=a.2451818308084.2124952.1630805309">be featured in a magazine</a>. After the second workshop I made a tutorial:</p>

<div style="text-align:center;">
<div class="video-embed"><iframe src="https://www.youtube-nocookie.com/embed/gC3BZJyvbIY" title="YouTube video" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>
</div>

<p>The workshop was very popular so I was invited for a follow up at<a href="http://2015.iconfestival.org.il/"> Icon 2015</a>, this time building a pencil crossbow:</p>

<div style="text-align:center;">
<div class="video-embed"><iframe src="https://www.youtube-nocookie.com/embed/6he5aKKcLL8" title="YouTube video" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>
</div>

<h3><strong><span style="text-decoration: underline;">Hearthstone tutorials</span></strong></h3>

<p>I’ve been playing collectible card games since I was 13 (notably Magic The Gathering). In addition to the hours of fun and great friends this hobby provided, it also taught me about strategic thinking, statistical analysis and “never quit” mentality – all at a young age. When I got access to the closed beta phase of Hearthstone, Blizzard’s online CCG, I was very excited and once I learned to play well – decided to create a series of tutorials for beginners:</p>

<div style="text-align:center;">
<div class="video-embed"><iframe src="https://www.youtube-nocookie.com/embed/7yk7QTZ5AGI?list=PLb9_LEV47z6vjPW5Ja8LwmoSrAlYdUI_c" title="YouTube video" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>
</div>

""",
    },
    {
        "title": 'Ideas',
        "slug": 'ideas-2',
        "order": 6,
        "body_html": r"""
<h4><a href="http://lifeinagraph.shalyt.com"><strong><span style="text-decoration: underline;">Life in a Graph</span></strong></a></h4>

<p>“Thoughts about the universe, drawn on x-y axis.”</p>

<p>Perhaps it’s my gaming background – or maybe my love for physics and probabilistic processes – but I have a tendency to think about various aspects of life in mathematical terms. Among&nbsp; the topics I covered in this blog/collection of essays are cost-efficient choices, psychological motivation tricks and game design analysis – to name a few.</p>

<h4><strong><span style="text-decoration: underline;">The Weekly Idea</span></strong></h4>

<p>Ever since I started getting involved in the startup community and business, I was a firm believer that ideas are cheap. Even if you thought about something that at least sounds like something people would want, your company and product can still fail in a myriad of ways. So, both in order to "prove" this view and to train my mind in spotting products that should exist but don't, I've created a closed mailing list of friends and colleagues and sent an idea for a product/startup/service every weekend - getting feedback and evolving the idea further. I kept it up for about 9 months, at which point I felt like I proved the point (at least to myself :) ).</p>

<p>That was several years ago. Since then 3 of the ideas were brought to life by startup companies I’ve heard about (and perhaps more by companies I didn’t).&nbsp;</p>

<h4><a href="http://brutalmotivation.shalyt.com"><strong><span style="text-decoration: underline;">Brutal Motivation</span></strong></a></h4>

<p>“If the wind will not serve, take to the oars.” – Latin Proverb.</p>

<p>I do not tend to publish my inner thoughts and feelings – this collection being the exception. In this blog I curate various quotes, music, videos, images, stories, articles etc. that motivate me to break through obstacles, to work harder and to fight for the right to build my own destiny. I explained the reason for creating it in the<a href="http://brutalmotivation.shalyt.com/2014/09/origins.html"> first post</a> so I won’t reiterate it here – I just hope some of the content makes you feel the same way I do.<br></p>

<h4><a href="http://albert.shalyt.com"><strong><span style="text-decoration: underline;">Commemoration site for my father (Albert Shalyt)</span></strong></a></h4>

<p>My dad once said to a good friend of his that in the age of the internet the way to commemorate someone is not via a tombstone in a graveyard – but with a public website containing his achievements and creations. After he died I decided it’s a good idea to do exactly that. The site I’ve created is far from summarizing all of my father’s life and work but it showcases some of what I found in his archives.<br></p>

""",
    },
]
