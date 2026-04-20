"""Rebuild Interactive map.html as a scrollytelling webpage, preserving all JS/data."""
import re

with open('Interactive map.html', 'r', encoding='utf-8') as f:
    original = f.read()

# Extract the JS block (everything from <script> IIFE to </script>)
js_match = re.search(r'(<script>\s*\(function\(\)\{.*?\}\)\(\);\s*</script>)', original, re.DOTALL)
if not js_match:
    raise RuntimeError("Could not find JS block")
js_block = js_match.group(1)

new_html = r'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HK Tropical Cyclone Impact &mdash; Scrollytelling</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"><\/script>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"><\/script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <link href="https://cdn.jsdelivr.net/npm/nouislider@15.7.1/dist/nouislider.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/nouislider@15.7.1/dist/nouislider.min.js"><\/script>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family:'Segoe UI',Roboto,sans-serif; background:#f0f4f8; color:#1e3a5f; }

        /* === HERO === */
        .hero {
            min-height:100vh; display:flex; flex-direction:column;
            justify-content:center; align-items:center; text-align:center;
            background:linear-gradient(160deg,#0a1929 0%,#1a3a5c 40%,#2c5a8a 100%);
            color:white; padding:60px 20px; position:relative; overflow:hidden;
        }
        .hero::before {
            content:''; position:absolute; inset:0;
            background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100'%3E%3Ccircle cx='50' cy='50' r='40' fill='none' stroke='rgba(255,255,255,0.03)' stroke-width='1'/%3E%3C/svg%3E");
            animation: heroSpin 120s linear infinite;
        }
        @keyframes heroSpin { to { transform:rotate(360deg); } }
        .hero h1 { font-size:clamp(2rem,5vw,3.4rem); font-weight:800; letter-spacing:-0.5px; line-height:1.15; max-width:800px; position:relative; }
        .hero h1 span { color:#f39c12; }
        .hero .subtitle { font-size:clamp(0.95rem,2vw,1.2rem); opacity:0.8; margin-top:16px; max-width:620px; line-height:1.6; position:relative; }
        .hero .scroll-cue {
            margin-top:48px; position:relative; animation:bounce 2s ease-in-out infinite;
            font-size:0.85rem; opacity:0.6; display:flex; flex-direction:column; align-items:center; gap:6px;
        }
        .hero .scroll-cue i { font-size:1.4rem; }
        @keyframes bounce {
            0%,100% { transform:translateY(0); }
            50% { transform:translateY(10px); }
        }

        /* === SECTION NARRATIVE === */
        .story-section {
            max-width:1400px; margin:0 auto; padding:0 20px;
            opacity:0; transform:translateY(40px);
            transition:opacity 0.7s ease, transform 0.7s ease;
        }
        .story-section.visible {
            opacity:1; transform:translateY(0);
        }
        .narrative {
            max-width:760px; margin:60px auto 28px;
            text-align:center; padding:0 16px;
        }
        .narrative .section-number {
            display:inline-block; width:36px; height:36px; line-height:36px;
            border-radius:50%; background:#1e3a5f; color:white;
            font-size:0.85rem; font-weight:700; margin-bottom:12px;
        }
        .narrative h2 {
            font-size:clamp(1.3rem,3vw,1.8rem); font-weight:700;
            color:#1e3a5f; margin-bottom:10px; line-height:1.3;
        }
        .narrative p {
            font-size:0.95rem; line-height:1.75; color:#4a627a;
        }
        .narrative .insight {
            margin-top:14px; padding:12px 18px;
            background:linear-gradient(135deg,#eef4fa,#f8fbff);
            border-left:4px solid #f39c12; border-radius:0 10px 10px 0;
            font-size:0.88rem; color:#1e3a5f; text-align:left;
        }
        .narrative .insight i { color:#f39c12; margin-right:6px; }

        /* === CONTROLS & WIDGETS === */
        .main-content { max-width:1400px; margin:0 auto; padding:0 20px; }

        .stats-row { display:flex; gap:12px; margin-bottom:16px; flex-wrap:wrap; }
        .stat-card {
            background:white; border-radius:12px; padding:14px 18px;
            flex:1; min-width:120px; box-shadow:0 2px 8px rgba(0,0,0,0.06);
        }
        .stat-card .label { font-size:0.72rem; color:#5f7d9c; text-transform:uppercase; letter-spacing:0.5px; }
        .stat-card .value { font-size:1.6rem; font-weight:700; color:#1e3a5f; }

        .controls-bar {
            background:white; border-radius:12px; padding:14px 20px;
            margin-bottom:16px; box-shadow:0 2px 8px rgba(0,0,0,0.06);
            display:flex; align-items:center; gap:16px; flex-wrap:wrap;
        }
        .controls-bar label { font-size:0.85rem; color:#1e3a5f; font-weight:600; }
        .controls-bar select {
            padding:6px 14px; border-radius:20px; border:1px solid #b0c7de;
            font-size:0.82rem; font-weight:500; background:white; cursor:pointer;
        }
        .btn-toggle {
            padding:6px 14px; border-radius:20px; border:1px solid #b0c7de;
            background:white; cursor:pointer; font-size:0.8rem; font-weight:500;
            transition:all 0.2s;
        }
        .btn-toggle.active { background:#1e3a5f; color:white; border-color:#1e3a5f; }
        .btn-toggle:hover:not(.active) { background:#e8f0f8; }

        .timeline-box {
            background:white; border-radius:12px; padding:14px 20px;
            margin-bottom:16px; box-shadow:0 2px 8px rgba(0,0,0,0.06);
        }
        .timeline-box .row { display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; }
        .timeline-box .row span { font-size:0.85rem; color:#1e3a5f; font-weight:600; }
        .year-display { color:#b02c2c !important; font-weight:700 !important; }
        #timeline-slider { margin:6px 0; }
        .noUi-connect { background:#1e3a5f; }
        .noUi-handle { border-color:#1e3a5f; }
        .noUi-horizontal { height:10px; }
        .noUi-horizontal .noUi-handle { width:22px; height:22px; top:-7px; right:-11px; border-radius:50%; }
        .noUi-handle:before,.noUi-handle:after { display:none; }

        /* Map */
        .map-wrapper {
            position:relative; border-radius:14px; overflow:hidden;
            margin-bottom:16px; box-shadow:0 3px 12px rgba(0,0,0,0.1);
        }
        #map { width:100%; height:480px; }
        .map-legend {
            position:absolute; top:12px; right:12px; z-index:1000;
            background:rgba(255,255,255,0.95); border-radius:10px;
            padding:10px 14px; box-shadow:0 2px 8px rgba(0,0,0,0.15);
            font-size:0.75rem; line-height:1.6;
        }
        .legend-dot {
            display:inline-block; width:10px; height:10px; border-radius:50%;
            margin-right:5px; vertical-align:middle;
        }
        #mapMarkerCount {
            position:absolute; bottom:12px; left:12px; z-index:1000;
            background:rgba(255,255,255,0.92); padding:6px 14px; border-radius:20px;
            font-size:0.8rem; font-weight:600; color:#1e3a5f;
            box-shadow:0 2px 6px rgba(0,0,0,0.12);
        }

        /* Charts */
        .charts-grid { display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:16px; }
        .chart-card {
            background:white; border-radius:14px; padding:14px;
            box-shadow:0 3px 10px rgba(0,0,0,0.05);
        }
        .chart-card h3 {
            font-size:0.92rem; color:#1e3a5f; margin-bottom:8px;
            display:flex; align-items:center; gap:6px;
        }
        .chart-card h3 i { color:#b02c2c; font-size:0.85rem; }
        .chart-area { width:100%; height:320px; }
        .chart-card.full-width { grid-column:1/-1; }
        .chart-card.full-width .chart-area { height:360px; }

        /* Info section */
        .info-card {
            background:white; border-radius:14px; padding:24px 28px;
            box-shadow:0 3px 10px rgba(0,0,0,0.05); margin-bottom:16px;
            font-size:0.85rem; color:#4a627a; line-height:1.8;
        }
        .info-card b { color:#1e3a5f; }

        /* Divider */
        .section-divider {
            width:60px; height:4px; background:linear-gradient(90deg,#1e3a5f,#f39c12);
            border-radius:2px; margin:60px auto 0;
        }

        footer {
            text-align:center; padding:40px 20px 20px;
            font-size:0.78rem; color:#7f9ab5; max-width:600px; margin:0 auto;
            border-top:1px solid #dde6ef; line-height:1.6;
        }

        @media (max-width:900px) {
            .charts-grid { grid-template-columns:1fr; }
            #map { height:350px; }
            .narrative { margin:40px auto 20px; }
        }
    </style>
</head>
<body>

<!-- ============ HERO ============ -->
<section class="hero">
    <h1>When the <span>Storm</span> Hits Hong Kong</h1>
    <p class="subtitle">
        An interactive data story exploring 35 years of tropical cyclone impacts on Hong Kong &mdash;
        from deadly super typhoons to shifting climate patterns. Based on 207 cyclone records from the Hong Kong Observatory (1988&ndash;2023).
    </p>
    <div class="scroll-cue">
        Scroll to begin
        <i class="fas fa-chevron-down"></i>
    </div>
</section>

<!-- ============ SECTION 1 &mdash; OVERVIEW ============ -->
<div class="section-divider"></div>
<section class="story-section">
    <div class="narrative">
        <span class="section-number">1</span>
        <h2>The Big Picture</h2>
        <p>
            Between 1988 and 2023, Hong Kong was affected by <b>207 tropical cyclones</b>.
            These storms brought destructive winds, torrential rain, dangerous storm surges, and billions of dollars in economic losses.
            The five summary cards below give you an instant snapshot of the overall toll. Use the <b>timeline slider</b> below to focus on any year range, and the <b>signal filter</b> to isolate storms of a particular intensity.
        </p>
        <div class="insight">
            <i class="fas fa-lightbulb"></i>
            <b>Try it:</b> Slide the timeline to a narrow range &mdash; say 2017&ndash;2018 &mdash; to see how a single season can dominate decades of statistics.
        </div>
    </div>

    <div class="main-content">
        <div class="stats-row">
            <div class="stat-card"><span class="label">Cyclones</span><div class="value" id="totalPassages">&mdash;</div></div>
            <div class="stat-card"><span class="label">Total Loss (HK$M)</span><div class="value" id="totalLoss">&mdash;</div></div>
            <div class="stat-card"><span class="label">Peak Surge (m)</span><div class="value" id="peakSurge">&mdash;</div></div>
            <div class="stat-card"><span class="label">Deaths</span><div class="value" id="totalDeaths">&mdash;</div></div>
            <div class="stat-card"><span class="label">Max Gust (km/h)</span><div class="value" id="maxGust">&mdash;</div></div>
        </div>
        <div class="timeline-box">
            <div class="row">
                <span><i class="fas fa-clock"></i> Timeline Range</span>
                <span class="year-display" id="yearDisplay">1988 &ndash; 2023</span>
            </div>
            <div id="timeline-slider"></div>
        </div>
        <div class="controls-bar">
            <label><i class="fas fa-eye"></i> Map View:</label>
            <button class="btn-toggle active" data-view="cyclones">Cyclones</button>
            <button class="btn-toggle" data-view="wind">Avg Wind</button>
            <button class="btn-toggle" data-view="rain">Avg Rainfall</button>
            <span style="width:1px;height:20px;background:#ddd;"></span>
            <label><i class="fas fa-filter"></i> Signal:</label>
            <select id="signalFilter">
                <option value="all">All Signals</option>
                <option value="1,3">Signal 1 / 3</option>
                <option value="8">Signal 8</option>
                <option value="9,10">Signal 9 / 10</option>
            </select>
            <span style="margin-left:auto;font-size:0.78rem;color:#7f9ab5;" id="dataStatus"></span>
        </div>
    </div>
</section>

<!-- ============ SECTION 2 &mdash; MAP ============ -->
<div class="section-divider"></div>
<section class="story-section">
    <div class="narrative">
        <span class="section-number">2</span>
        <h2>Where Do the Storms Go?</h2>
        <p>
            Each circle on the map marks the closest point of approach of a tropical cyclone relative to the Hong Kong Observatory.
            <b>Green dots</b> are lower-signal storms (1 or 3), <b>orange</b> marks Signal 8 (gale), and <b>red</b> marks the most
            dangerous Signal 9 and 10 events. The size of each dot reflects economic loss.
        </p>
        <p style="margin-top:10px;">
            Switch to <b>Avg Wind</b> or <b>Avg Rainfall</b> view to see how weather stations across Hong Kong
            experience different average conditions &mdash; coastal stations like Waglan Island and Cheung Chau
            consistently record the strongest gusts, while mountainous areas catch the heaviest rain.
        </p>
        <div class="insight">
            <i class="fas fa-lightbulb"></i>
            <b>Key insight:</b> Storms approaching from the south and southwest tend to cause the highest surges because they push water directly into Victoria Harbour.
        </div>
    </div>

    <div class="main-content">
        <div class="map-wrapper">
            <div id="map"></div>
            <div class="map-legend" id="mapLegend">
                <div style="font-weight:600;margin-bottom:4px;">Cyclone Signals</div>
                <div><span class="legend-dot" style="background:#2ecc71"></span> Signal 1/3</div>
                <div><span class="legend-dot" style="background:#f39c12"></span> Signal 8</div>
                <div><span class="legend-dot" style="background:#e74c3c"></span> Signal 9/10</div>
            </div>
            <div id="mapMarkerCount"></div>
        </div>
    </div>
</section>

<!-- ============ SECTION 3 &mdash; FREQUENCY ============ -->
<div class="section-divider"></div>
<section class="story-section">
    <div class="narrative">
        <span class="section-number">3</span>
        <h2>How Often Do Typhoons Strike?</h2>
        <p>
            This stacked bar chart shows how many tropical cyclones affected Hong Kong each year,
            broken down by signal level. Most years see 4&ndash;8 events, but the severity mix varies widely.
            Some years (like 1993 and 1999) saw clusters of strong storms, while others passed relatively quietly.
        </p>
        <div class="insight">
            <i class="fas fa-lightbulb"></i>
            <b>What to look for:</b> Notice how the proportion of red and orange bars (higher signals) is not increasing over time &mdash; while climate change is expected to intensify individual storms, it hasn't yet produced a clear upward trend in the frequency of severe warnings in Hong Kong.
        </div>
    </div>

    <div class="main-content">
        <div class="charts-grid">
            <div class="chart-card full-width">
                <h3><i class="fas fa-chart-bar"></i> Typhoon Frequency by Year</h3>
                <div class="chart-area" id="freqChart"></div>
            </div>
        </div>
    </div>
</section>

<!-- ============ SECTION 4 &mdash; RADAR & BOXPLOT ============ -->
<div class="section-divider"></div>
<section class="story-section">
    <div class="narrative">
        <span class="section-number">4</span>
        <h2>Comparing Impact Dimensions</h2>
        <p>
            Not all typhoons are created equal. The <b>radar chart</b> compares the average profile of storms
            at each signal level across five dimensions: wind gust, rainfall, storm surge, economic loss, and
            people affected. Higher-signal storms clearly dominate across every axis &mdash; but loss and affected
            counts spike <em>disproportionately</em> for Signal 9/10 events.
        </p>
        <p style="margin-top:10px;">
            The <b>box plot</b> shows how economic losses are distributed within each signal group.
            The wide range of outliers for Signal 8 reflects the fact that many factors beyond wind speed &mdash;
            rainfall, timing, storm surge, and track &mdash; determine the final damage.
        </p>
        <div class="insight">
            <i class="fas fa-lightbulb"></i>
            <b>Key insight:</b> Signal 9/10 storms cause losses that are on average 10&times; higher than Signal 8 storms.
            The jump from Signal 8 to 9 represents a threshold where damage becomes catastrophic.
        </div>
    </div>

    <div class="main-content">
        <div class="charts-grid">
            <div class="chart-card">
                <h3><i class="fas fa-chart-pie"></i> Multi-dimensional Impact</h3>
                <div class="chart-area" id="radarChart"></div>
            </div>
            <div class="chart-card">
                <h3><i class="fas fa-box"></i> Loss Distribution by Signal</h3>
                <div class="chart-area" id="boxplotChart"></div>
            </div>
        </div>
    </div>
</section>

<!-- ============ SECTION 5 &mdash; BUBBLE ============ -->
<div class="section-divider"></div>
<section class="story-section">
    <div class="narrative">
        <span class="section-number">5</span>
        <h2>The Economic Toll &mdash; A Rising Trend?</h2>
        <p>
            Each bubble represents a cyclone that caused measurable economic loss. The vertical axis uses
            a <b>logarithmic scale</b> &mdash; so each grid line represents a 10&times; increase in damage.
            Bubble size reflects the number of people affected, and colour indicates the signal level.
        </p>
        <p style="margin-top:10px;">
            The most striking feature is <b>Super Typhoon Mangkhut (2018)</b>, sitting at the very top with
            HK$4.6 billion in estimated damages. But notice how recent years (2019&ndash;2023) have several
            high-loss events &mdash; suggesting that even moderate storms now cause more economic disruption
            as Hong Kong's built environment grows denser and more valuable.
        </p>
        <div class="insight">
            <i class="fas fa-lightbulb"></i>
            <b>What to look for:</b> Hover over any bubble to see detailed storm information. The labelled names help you identify the most notorious storms. Note how Typhoon York (1999), Typhoon Vicente (2012), and Typhoon Hato (2017) each represented the worst event of their respective decades.
        </div>
    </div>

    <div class="main-content">
        <div class="charts-grid">
            <div class="chart-card full-width">
                <h3><i class="fas fa-coins"></i> Economic Loss vs Year</h3>
                <div class="chart-area" id="bubbleChart" style="height:380px;"></div>
            </div>
        </div>
    </div>
</section>

<!-- ============ SECTION 6 &mdash; CASUALTIES ============ -->
<div class="section-divider"></div>
<section class="story-section">
    <div class="narrative">
        <span class="section-number">6</span>
        <h2>The Human Cost</h2>
        <p>
            Behind every statistic is a human story. This chart tracks <b>deaths</b> (red bars),
            <b>injuries</b> (orange bars), and <b>people affected</b> (blue line, scaled &divide;10)
            across the 35-year period. The good news: fatalities have generally declined, reflecting
            improved forecasting, better building codes, and an effective warning system.
        </p>
        <p style="margin-top:10px;">
            However, the number of <b>people affected</b> has risen sharply in recent events like
            Mangkhut (2018) and Haikui (2023), as population density increases and
            more infrastructure is exposed to storm surges and flooding.
        </p>
        <div class="insight">
            <i class="fas fa-lightbulb"></i>
            <b>Key insight:</b> While deaths have declined from an average of ~5/year in the 1990s to near zero in recent years, the affected population has surged &mdash; showing that Hong Kong is better at saving lives but increasingly vulnerable to disruption.
        </div>
    </div>

    <div class="main-content">
        <div class="charts-grid">
            <div class="chart-card full-width">
                <h3><i class="fas fa-user-injured"></i> Casualties &amp; Affected Over Time</h3>
                <div class="chart-area" id="casualtyChart"></div>
            </div>
        </div>
    </div>
</section>

<!-- ============ SECTION 7 &mdash; SIGNAL SYSTEM ============ -->
<div class="section-divider"></div>
<section class="story-section">
    <div class="narrative">
        <span class="section-number">7</span>
        <h2>Understanding the Warning System</h2>
        <p>
            Hong Kong's tropical cyclone warning system is one of the most recognised in Asia.
            Signals range from 1 (standby) to 10 (hurricane-force winds), and each level triggers
            specific actions across the city &mdash; from school closures to full transport shutdowns.
        </p>
    </div>

    <div class="main-content">
        <div class="info-card">
            <span class="legend-dot" style="background:#2ecc71"></span> <b>Signal 1 (Standby)</b> &ndash; A tropical cyclone is within 800 km of Hong Kong. Stay alert and monitor updates.<br><br>
            <span class="legend-dot" style="background:#2ecc71"></span> <b>Signal 3 (Strong Wind)</b> &ndash; Sustained winds of 41&ndash;62 km/h expected. Secure loose outdoor items.<br><br>
            <span class="legend-dot" style="background:#f39c12"></span> <b>Signal 8 (Gale or Storm)</b> &ndash; Winds 63&ndash;117 km/h. Schools and offices close. All should stay indoors.<br><br>
            <span class="legend-dot" style="background:#e74c3c"></span> <b>Signal 9 (Increasing Gale)</b> &ndash; Significant intensification imminent. Extreme danger outdoors.<br><br>
            <span class="legend-dot" style="background:#e74c3c"></span> <b>Signal 10 (Hurricane)</b> &ndash; Sustained winds &ge;118 km/h. Maximum destructive force. Most severe warning in HK.
            <br><br>
            <div style="background:linear-gradient(135deg,#eef4fa,#f8fbff);padding:14px 18px;border-radius:10px;margin-top:10px;">
                <b style="color:#b02c2c;">Did you know?</b> Super Typhoon Mangkhut (2018) caused an estimated HK$4.6 billion in damage &mdash; the costliest
                tropical cyclone in Hong Kong's modern history. Signal 10 was hoisted, and storm surge reached 2.35m above normal.
            </div>
        </div>
    </div>
</section>

<footer>
    Data source: Hong Kong Observatory Tropical Cyclone Impact Dataset &middot; 1988&ndash;2023 &middot; Losses in nominal HK$ millions<br>
    Created for COMP4462 Data Visualization Project
</footer>

'''

# Now append the original JS block
new_html += js_block + '\n'

# Add scroll observer script
new_html += r'''
<script>
(function(){
    var sections = document.querySelectorAll('.story-section');
    var observer = new IntersectionObserver(function(entries){
        entries.forEach(function(entry){
            if(entry.isIntersecting){
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.08 });
    sections.forEach(function(s){ observer.observe(s); });
})();
</script>
</body>
</html>
'''

# Fix escaped script tags
new_html = new_html.replace('<\\/script>', '</script>')

with open('Interactive map.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Done! Scrollytelling version written to Interactive map.html")
print(f"File size: {len(new_html):,} bytes")
