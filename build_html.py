import json

with open('cyclones_embed.txt','r',encoding='utf-8-sig') as f: cyclones_json = f.read().strip()
with open('wind_embed.txt','r',encoding='utf-8-sig') as f: wind_json = f.read().strip()
with open('rain_embed.txt','r',encoding='utf-8-sig') as f: rain_json = f.read().strip()

html = r'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HK Tropical Cyclone Impact Dashboard</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"><\/script>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"><\/script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <link href="https://cdn.jsdelivr.net/npm/nouislider@15.7.1/dist/nouislider.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/nouislider@15.7.1/dist/nouislider.min.js"><\/script>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family:'Segoe UI',Roboto,sans-serif; background:#f0f4f8; }
        header {
            background:linear-gradient(135deg,#1a2a3a 0%,#2c4a6a 100%);
            color:white; padding:18px 28px; display:flex; align-items:center; gap:14px;
        }
        header h1 { font-size:1.4rem; font-weight:700; }
        header p { font-size:0.82rem; opacity:0.8; }

        .main-content { max-width:1400px; margin:0 auto; padding:16px 20px; }

        /* Stats row */
        .stats-row { display:flex; gap:12px; margin-bottom:16px; flex-wrap:wrap; }
        .stat-card {
            background:white; border-radius:12px; padding:14px 18px;
            flex:1; min-width:120px; box-shadow:0 2px 8px rgba(0,0,0,0.06);
        }
        .stat-card .label { font-size:0.72rem; color:#5f7d9c; text-transform:uppercase; letter-spacing:0.5px; }
        .stat-card .value { font-size:1.6rem; font-weight:700; color:#1e3a5f; }

        /* Controls bar */
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

        /* Timeline */
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

        /* Charts grid */
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
            background:white; border-radius:14px; padding:18px;
            box-shadow:0 3px 10px rgba(0,0,0,0.05); margin-bottom:16px;
            font-size:0.82rem; color:#4a627a; line-height:1.8;
        }
        .info-card b { color:#1e3a5f; }
        footer { text-align:center; padding:10px; font-size:0.72rem; color:#7f9ab5; }

        @media (max-width:900px) {
            .charts-grid { grid-template-columns:1fr; }
            #map { height:350px; }
        }
    </style>
</head>
<body>
<header>
    <i class="fas fa-bolt" style="font-size:1.6rem;"></i>
    <div>
        <h1>Hong Kong Typhoon Impact Dashboard</h1>
        <p>Interactive analysis of tropical cyclone impacts &middot; 1988&ndash;2023 &middot; 207 cyclones</p>
    </div>
</header>

<div class="main-content">
    <!-- Stats -->
    <div class="stats-row">
        <div class="stat-card"><span class="label">Cyclones</span><div class="value" id="totalPassages">&mdash;</div></div>
        <div class="stat-card"><span class="label">Total Loss (HK$M)</span><div class="value" id="totalLoss">&mdash;</div></div>
        <div class="stat-card"><span class="label">Peak Surge (m)</span><div class="value" id="peakSurge">&mdash;</div></div>
        <div class="stat-card"><span class="label">Deaths</span><div class="value" id="totalDeaths">&mdash;</div></div>
        <div class="stat-card"><span class="label">Max Gust (km/h)</span><div class="value" id="maxGust">&mdash;</div></div>
    </div>

    <!-- Timeline -->
    <div class="timeline-box">
        <div class="row">
            <span><i class="fas fa-clock"></i> Timeline Range</span>
            <span class="year-display" id="yearDisplay">1988 &ndash; 2023</span>
        </div>
        <div id="timeline-slider"></div>
    </div>

    <!-- Controls -->
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

    <!-- Map -->
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

    <!-- Charts -->
    <div class="charts-grid">
        <div class="chart-card full-width">
            <h3><i class="fas fa-chart-bar"></i> Typhoon Frequency by Year</h3>
            <div class="chart-area" id="freqChart"></div>
        </div>
        <div class="chart-card">
            <h3><i class="fas fa-chart-pie"></i> Multi-dimensional Impact</h3>
            <div class="chart-area" id="radarChart"></div>
        </div>
        <div class="chart-card">
            <h3><i class="fas fa-box"></i> Loss Distribution by Signal</h3>
            <div class="chart-area" id="boxplotChart"></div>
        </div>
        <div class="chart-card full-width">
            <h3><i class="fas fa-coins"></i> Economic Loss vs Year</h3>
            <div class="chart-area" id="bubbleChart" style="height:380px;"></div>
        </div>
        <div class="chart-card full-width">
            <h3><i class="fas fa-user-injured"></i> Casualties &amp; Affected Over Time</h3>
            <div class="chart-area" id="casualtyChart"></div>
        </div>
    </div>

    <!-- Educational info -->
    <div class="info-card">
        <b style="font-size:0.95rem;">Understanding Hong Kong's Typhoon Signal System</b><br><br>
        <span class="legend-dot" style="background:#2ecc71"></span> <b>Signal 1 (Standby)</b> &ndash; A tropical cyclone is within 800 km of Hong Kong. Stay alert and monitor updates.<br>
        <span class="legend-dot" style="background:#2ecc71"></span> <b>Signal 3 (Strong Wind)</b> &ndash; Sustained winds of 41&ndash;62 km/h expected. Secure loose outdoor items.<br>
        <span class="legend-dot" style="background:#f39c12"></span> <b>Signal 8 (Gale or Storm)</b> &ndash; Winds 63&ndash;117 km/h. Schools and offices close. All should stay indoors.<br>
        <span class="legend-dot" style="background:#e74c3c"></span> <b>Signal 9 (Increasing Gale)</b> &ndash; Significant intensification imminent. Extreme danger outdoors.<br>
        <span class="legend-dot" style="background:#e74c3c"></span> <b>Signal 10 (Hurricane)</b> &ndash; Sustained winds &ge;118 km/h. Maximum destructive force. Most severe warning in HK.
        <br><br>
        <b>Did you know?</b> Super Typhoon Mangkhut (2018) caused an estimated HK$4.6 billion in damage &mdash; the costliest
        tropical cyclone in Hong Kong's modern history. Signal 10 was hoisted, and storm surge reached 2.35m above normal.
    </div>
</div>
<footer>Data source: Hong Kong Observatory Tropical Cyclone Impact Dataset &middot; Losses in nominal HK$ millions</footer>

<script>
(function(){
    var HKO_LAT=22.302,HKO_LON=114.174;
    var bearingMap={'N':0,'NNE':22.5,'NE':45,'ENE':67.5,'E':90,'ESE':112.5,'SE':135,'SSE':157.5,'S':180,'SSW':202.5,'SW':225,'WSW':247.5,'W':270,'WNW':292.5,'NW':315,'NNW':337.5};

    var STATION_COORDS={
        'Shatin':[22.399,114.185],'Sha Tin':[22.399,114.185],'Sha Tin Stations':[22.399,114.185],
        'Lau Fau Shan':[22.469,113.982],'Ta Kwu Ling':[22.528,114.157],
        'Cheung Chau':[22.201,114.027],'Cheung Chau Stations':[22.201,114.027],
        'Sai Kung':[22.375,114.274],'Sai Kung Station':[22.375,114.274],
        'Tsing Yi':[22.344,114.110],'Tsing Yi Station':[22.344,114.110],
        'Kai Tak':[22.311,114.214],'Chek Lap Kok':[22.309,113.922],
        'Waglan Island':[22.182,114.303],'Tuen Mun':[22.386,113.964],
        'Tuen Mun Station':[22.386,113.964],'Tuen Mun Reservoir Station':[22.404,113.955],
        'Tai Mo Shan':[22.411,114.124],'Tai Mo Shan Station':[22.411,114.124],
        "Tate's Cairn":[22.358,114.218],'Green Island':[22.285,114.112],
        'Star Ferry (Tsim Sha Tsui)':[22.294,114.169],
        'Wong Chuk Hang':[22.248,114.174],'Sha Lo Wan':[22.282,113.905],
        'Tseung Kwan O':[22.316,114.259],"King's Park":[22.312,114.173],
        'Ping Chau':[22.536,114.296],'Tai Mei Tuk':[22.475,114.237],
        'Tai Mei Tuk Station':[22.475,114.237],
        'North Point':[22.291,114.200],'North Point Station':[22.291,114.200],
        'Shek Kong':[22.436,114.085],'Shek Kong Stations':[22.436,114.085],
        'Sha Chau':[22.351,113.890],'Ngong Ping':[22.259,113.914],
        'Peng Chau':[22.289,114.040],'Wetland Park':[22.467,114.008],
        'Central Pier':[22.287,114.160],'Cheung Chau Beach':[22.209,114.023],
        'Tai Po Kau':[22.427,114.182],'Lamma Island':[22.222,114.113],
        'Tap Mun East (Tap Mun 2014)':[22.471,114.361],
        'Bluff Head (Stanley)':[22.219,114.219],
        'Hong Kong International Airport Stations':[22.309,113.922],
        'Aberdeen Station':[22.248,114.155],'Fanling Station':[22.492,114.138],
        'High Island Station':[22.370,114.347],'Jordan Valley Station':[22.326,114.225],
        'Kwai Chung Station':[22.357,114.129],'Mid Levels Stations':[22.279,114.151],
        'Shau Kei Wan Station':[22.279,114.228],'So Uk Estate Station':[22.335,114.160],
        'Tap Shek Kok Station':[22.453,114.180],'Tung Chung Station':[22.289,113.944],
        'Ap Lei Chau Station':[22.242,114.153],'Au Tau Station':[22.454,114.049],
        "Cape D'Aguilar Station":[22.209,114.260],'Causeway Bay Station':[22.280,114.185],
        'Central Station':[22.282,114.158],'Discovery Bay Station':[22.294,114.015],
        'Happy Valley Station':[22.271,114.183],'Kwun Tong Station':[22.312,114.226],
        'Lantau Stations':[22.260,113.950],'Repulse Bay Station':[22.237,114.198],
        'Pokfulam Station':[22.260,114.136],'Sha Tau Kok Station':[22.543,114.213],
        'Sok Kwu Wan Station':[22.206,114.128],'Stanley Station':[22.219,114.219],
        'Tai O Station':[22.254,113.860],'Tai Po Station':[22.450,114.164],
        'Tsuen Wan Station':[22.371,114.114],'Yuen Long Stations':[22.445,114.022],
        'Victoria Peak Station':[22.276,114.150],'HKO Headquarters':[22.302,114.174]
    };

    function destination(lat,lon,dKm,deg){
        var R=6371,lat1=lat*Math.PI/180,lon1=lon*Math.PI/180,brng=deg*Math.PI/180;
        var lat2=Math.asin(Math.sin(lat1)*Math.cos(dKm/R)+Math.cos(lat1)*Math.sin(dKm/R)*Math.cos(brng));
        var lon2=lon1+Math.atan2(Math.sin(brng)*Math.sin(dKm/R)*Math.cos(lat1),Math.cos(dKm/R)-Math.sin(lat1)*Math.sin(lat2));
        return{lat:lat2*180/Math.PI,lng:lon2*180/Math.PI};
    }

    // ===== DATA =====
    var allCyclones = ''' + "CYCLONES_PLACEHOLDER" + r''';
    var windStationData = ''' + "WIND_PLACEHOLDER" + r''';
    var rainStationData = ''' + "RAIN_PLACEHOLDER" + r''';

    // Compute lat/lng for each cyclone
    allCyclones.forEach(function(c){
        if(c.distance && c.bearing){
            var deg=bearingMap[c.bearing.toUpperCase()]||0;
            var pos=destination(HKO_LAT,HKO_LON,c.distance,deg);
            c.lat=pos.lat; c.lng=pos.lng;
        }
    });

    // ===== STATE =====
    var currentView='cyclones', yearRange=[1988,2023], signalFilter='all';

    // ===== MAP =====
    var map=L.map('map').setView([22.35,114.10],10);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',{
        attribution:'&copy; OSM, CartoDB',subdomains:'abcd',maxZoom:19
    }).addTo(map);
    L.marker([HKO_LAT,HKO_LON],{
        icon:L.divIcon({className:'',html:'<div style="background:#1e466e;width:12px;height:12px;border-radius:50%;border:2px solid white;box-shadow:0 1px 4px rgba(0,0,0,0.3)"></div>',iconSize:[12,12],iconAnchor:[6,6]})
    }).addTo(map).bindTooltip('HK Observatory',{permanent:false});
    var tcLayer=L.layerGroup().addTo(map);

    function getFiltered(){
        return allCyclones.filter(function(c){
            if(c.year<yearRange[0]||c.year>yearRange[1]) return false;
            if(signalFilter!=='all'){
                var sigs=signalFilter.split(',').map(Number);
                if(sigs.indexOf(c.signal)<0) return false;
            }
            return true;
        });
    }

    function renderCycloneMap(){
        tcLayer.clearLayers();
        var filtered=getFiltered();
        filtered.forEach(function(c){
            if(!c.lat||!c.lng) return;
            var color=c.signal>=9?'#e74c3c':(c.signal===8?'#f39c12':'#2ecc71');
            var r=Math.min(8,Math.max(4,Math.sqrt(c.loss||0)*0.12+4));
            L.circleMarker([c.lat,c.lng],{
                radius:r,fillColor:color,color:'#fff',weight:1.5,fillOpacity:0.8
            }).addTo(tcLayer).bindPopup(
                '<b>'+c.name+' ('+c.year+')</b><br>'+
                '\u26A0\uFE0F Signal '+c.signal+'<br>'+
                '\uD83D\uDCCF '+c.distance+' km '+c.bearing+'<br>'+
                '\uD83D\uDCA8 Max Gust: '+(c.maxGust||'?')+' km/h<br>'+
                '\uD83C\uDF27\uFE0F Max Rain: '+(c.maxRain||'?')+' mm<br>'+
                '\uD83C\uDF0A Surge: '+(c.surge?c.surge.toFixed(2):'?')+' m<br>'+
                '\uD83D\uDCB0 Loss: HK$'+(c.loss||0).toFixed(1)+'M<br>'+
                '\uD83D\uDC65 Affected: '+(c.affected||0)
            );
        });
        document.getElementById('mapMarkerCount').innerText=filtered.length+' cyclones shown';
        updateLegend('cyclones');
    }

    function findCoords(name){
        if(STATION_COORDS[name]) return STATION_COORDS[name];
        var t=name.trim();
        if(STATION_COORDS[t]) return STATION_COORDS[t];
        var lo=t.toLowerCase().replace(/\s+/g,' ');
        for(var k in STATION_COORDS){
            var kl=k.toLowerCase().replace(/\s+/g,' ');
            if(kl.indexOf(lo)>=0||lo.indexOf(kl)>=0) return STATION_COORDS[k];
        }
        return null;
    }

    function renderStationMap(type){
        tcLayer.clearLayers();
        var filtered=getFiltered();
        var keys=filtered.map(function(c){return c.year+'_'+c.name;});
        var agg={};
        keys.forEach(function(key){
            var data=type==='wind'?windStationData[key]:rainStationData[key];
            if(!data) return;
            Object.keys(data).forEach(function(stn){
                var val=data[stn];
                if(!agg[stn]) agg[stn]={sum:0,count:0};
                var v=type==='wind'?((val&&val.gust)||0):(typeof val==='number'?val:0);
                if(v>0){agg[stn].sum+=v;agg[stn].count++;}
            });
        });
        var maxAvg=0;
        Object.keys(agg).forEach(function(s){if(agg[s].count>0) maxAvg=Math.max(maxAvg,agg[s].sum/agg[s].count);});
        var count=0;
        Object.keys(agg).forEach(function(stn){
            var s=agg[stn];
            var coords=findCoords(stn);
            if(!coords||s.count===0) return;
            var avg=s.sum/s.count;
            var ratio=maxAvg>0?avg/maxAvg:0;
            var color;
            if(type==='wind'){
                color='rgb('+Math.round(255*Math.min(1,ratio*2))+','+Math.round(255*Math.max(0,1-ratio*1.2))+',50)';
            } else {
                color='rgb('+Math.round(50*(1-ratio))+','+Math.round(100*(1-ratio))+','+Math.round(50+200*ratio)+')';
            }
            var radius=8+ratio*16;
            L.circleMarker(coords,{
                radius:radius,fillColor:color,color:'#fff',weight:1.5,fillOpacity:0.75
            }).addTo(tcLayer).bindPopup(
                '<b>'+stn.replace(/\n/g,' ').replace(/ Station[s]?$/i,'').trim()+'</b><br>'+
                (type==='wind'?'\uD83D\uDCA8 Avg Max Gust: <b>'+avg.toFixed(1)+' km/h</b>':
                '\uD83C\uDF27\uFE0F Avg Rainfall: <b>'+avg.toFixed(1)+' mm</b>')+
                '<br>Based on '+s.count+' cyclone(s)'
            );
            count++;
        });
        document.getElementById('mapMarkerCount').innerText=count+' stations shown';
        updateLegend(type);
    }

    function updateLegend(type){
        var el=document.getElementById('mapLegend');
        if(type==='cyclones'){
            el.innerHTML='<div style="font-weight:600;margin-bottom:4px;">Cyclone Signals</div>'+
                '<div><span class="legend-dot" style="background:#2ecc71"></span> Signal 1/3</div>'+
                '<div><span class="legend-dot" style="background:#f39c12"></span> Signal 8</div>'+
                '<div><span class="legend-dot" style="background:#e74c3c"></span> Signal 9/10</div>';
        } else if(type==='wind'){
            el.innerHTML='<div style="font-weight:600;margin-bottom:4px;">Avg Max Gust (km/h)</div>'+
                '<div style="background:linear-gradient(to right,rgb(0,255,50),rgb(255,200,50),rgb(255,0,50));height:12px;border-radius:4px;margin:4px 0;"></div>'+
                '<div style="display:flex;justify-content:space-between;font-size:0.7rem;"><span>Low</span><span>High</span></div>';
        } else {
            el.innerHTML='<div style="font-weight:600;margin-bottom:4px;">Avg Rainfall (mm)</div>'+
                '<div style="background:linear-gradient(to right,rgb(50,100,50),rgb(25,50,125),rgb(0,0,250));height:12px;border-radius:4px;margin:4px 0;"></div>'+
                '<div style="display:flex;justify-content:space-between;font-size:0.7rem;"><span>Low</span><span>High</span></div>';
        }
    }

    function renderMapView(){
        if(currentView==='cyclones') renderCycloneMap();
        else renderStationMap(currentView);
    }

    // ===== CHARTS =====
    var freqChart,radarChart,bubbleChart,boxplotChart,casualtyChart;
    function initCharts(){
        freqChart=echarts.init(document.getElementById('freqChart'));
        radarChart=echarts.init(document.getElementById('radarChart'));
        bubbleChart=echarts.init(document.getElementById('bubbleChart'));
        boxplotChart=echarts.init(document.getElementById('boxplotChart'));
        casualtyChart=echarts.init(document.getElementById('casualtyChart'));
    }

    function refreshAll(){
        var filtered=getFiltered();
        renderMapView();
        updateStats(filtered);
        updateFreqChart(filtered);
        updateRadarChart(filtered);
        updateBubbleChart(filtered);
        updateBoxplotChart(filtered);
        updateCasualtyChart(filtered);
        document.getElementById('dataStatus').innerText=filtered.length+' of '+allCyclones.length+' TCs';
    }

    function updateStats(f){
        document.getElementById('totalPassages').innerText=f.length;
        var tl=f.reduce(function(s,c){return s+c.loss;},0);
        document.getElementById('totalLoss').innerText=tl>=1000?(tl/1000).toFixed(1)+'B':tl.toFixed(0);
        var ms=f.length>0?Math.max.apply(null,f.map(function(c){return c.surge||0;})):0;
        document.getElementById('peakSurge').innerText=ms.toFixed(2);
        document.getElementById('totalDeaths').innerText=f.reduce(function(s,c){return s+(c.dead||0);},0);
        var mg=f.length>0?Math.max.apply(null,f.map(function(c){return c.maxGust||0;})):0;
        document.getElementById('maxGust').innerText=mg.toFixed(0);
    }

    function updateFreqChart(filtered){
        var ys={};
        filtered.forEach(function(c){
            if(!ys[c.year]) ys[c.year]={low:0,mid:0,high:0};
            if(c.signal<=3) ys[c.year].low++;
            else if(c.signal===8) ys[c.year].mid++;
            else ys[c.year].high++;
        });
        var years=[];for(var y=yearRange[0];y<=yearRange[1];y++) years.push(y);
        freqChart.setOption({
            tooltip:{trigger:'axis',axisPointer:{type:'shadow'}},
            legend:{data:['Signal 1/3','Signal 8','Signal 9/10'],bottom:0,textStyle:{fontSize:11}},
            grid:{left:40,right:15,top:10,bottom:40},
            xAxis:{type:'category',data:years,axisLabel:{fontSize:10,rotate:45}},
            yAxis:{type:'value',name:'Count',nameTextStyle:{fontSize:10},axisLabel:{fontSize:10},minInterval:1},
            series:[
                {name:'Signal 1/3',type:'bar',stack:'t',data:years.map(function(y){return(ys[y]||{}).low||0;}),itemStyle:{color:'#2ecc71'},barMaxWidth:22},
                {name:'Signal 8',type:'bar',stack:'t',data:years.map(function(y){return(ys[y]||{}).mid||0;}),itemStyle:{color:'#f39c12'},barMaxWidth:22},
                {name:'Signal 9/10',type:'bar',stack:'t',data:years.map(function(y){return(ys[y]||{}).high||0;}),itemStyle:{color:'#e74c3c'},barMaxWidth:22}
            ]
        },true);
    }

    function updateRadarChart(filtered){
        var groups={'1,3':[],'8':[],'9,10':[]};
        filtered.forEach(function(c){
            if(c.signal<=3) groups['1,3'].push(c);
            else if(c.signal===8) groups['8'].push(c);
            else groups['9,10'].push(c);
        });
        var colors={'1,3':'#2ecc71','8':'#f39c12','9,10':'#e74c3c'};
        var names={'1,3':'Signal 1/3','8':'Signal 8','9,10':'Signal 9/10'};
        var sd=[],allA={gust:[],rain:[],surge:[],loss:[],aff:[]};
        Object.keys(groups).forEach(function(key){
            var a=groups[key]; if(!a.length) return;
            var ag=a.reduce(function(s,c){return s+(c.maxGust||0);},0)/a.length;
            var ar=a.reduce(function(s,c){return s+(c.maxRain||0);},0)/a.length;
            var as2=a.reduce(function(s,c){return s+(c.surge||0);},0)/a.length;
            var al=a.reduce(function(s,c){return s+(c.loss||0);},0)/a.length;
            var aa=a.reduce(function(s,c){return s+(c.affected||0);},0)/a.length;
            allA.gust.push(ag);allA.rain.push(ar);allA.surge.push(as2);allA.loss.push(al);allA.aff.push(aa);
            sd.push({name:names[key],value:[ag,ar,as2,al,aa],areaStyle:{opacity:0.15},lineStyle:{width:2},itemStyle:{color:colors[key]}});
        });
        var mx=function(arr,min){return Math.max(min,Math.max.apply(null,arr.concat([0]))*1.3);};
        radarChart.setOption({
            tooltip:{trigger:'item',formatter:function(p){
                if(!p.value) return '';
                return '<b>'+p.name+'</b><br>Avg Gust: '+p.value[0].toFixed(1)+' km/h<br>Avg Rain: '+p.value[1].toFixed(1)+' mm<br>Avg Surge: '+p.value[2].toFixed(2)+' m<br>Avg Loss: HK$'+p.value[3].toFixed(1)+'M<br>Avg Affected: '+p.value[4].toFixed(0);
            }},
            legend:{bottom:0,textStyle:{fontSize:10}},
            radar:{
                indicator:[
                    {name:'Avg Gust\n(km/h)',max:mx(allA.gust,50)},
                    {name:'Avg Rain\n(mm)',max:mx(allA.rain,50)},
                    {name:'Avg Surge\n(m)',max:mx(allA.surge,0.3)},
                    {name:'Avg Loss\n(HK$M)',max:mx(allA.loss,1)},
                    {name:'Avg Affected',max:mx(allA.aff,5)}
                ],
                shape:'circle',radius:'55%',nameGap:10,axisName:{fontSize:9,color:'#5f7d9c'}
            },
            series:[{type:'radar',data:sd}]
        },true);
    }

    function updateBubbleChart(filtered){
        var data=[];
        filtered.forEach(function(c){
            if((c.loss||0)<=0&&(c.affected||0)<=0) return;
            data.push({
                value:[c.year,Math.max(0.01,c.loss||0.01),c.affected||1,c.signal,c.maxGust||0],
                tcName:c.name,tcYear:c.year,tcSignal:c.signal,
                itemStyle:{color:c.signal>=9?'rgba(231,76,60,0.7)':(c.signal===8?'rgba(243,156,18,0.7)':'rgba(46,204,113,0.7)')}
            });
        });
        bubbleChart.setOption({
            tooltip:{trigger:'item',formatter:function(p){
                return '<b>'+p.data.tcName+' ('+p.data.tcYear+')</b><br>Signal '+p.data.tcSignal+'<br>Loss: HK$'+p.value[1].toFixed(1)+'M<br>Affected: '+p.value[2]+'<br>Max Gust: '+p.value[4]+' km/h';
            }},
            grid:{left:60,right:20,top:30,bottom:45},
            xAxis:{name:'Year',type:'value',min:yearRange[0]-1,max:yearRange[1]+1,
                axisLabel:{fontSize:10,formatter:function(v){return v.toString();}},nameTextStyle:{fontSize:10}},
            yAxis:{name:'Loss (HK$M)',type:'log',min:0.01,
                axisLabel:{fontSize:10,formatter:function(v){return v>=1000?(v/1000)+'B':v>=1?v.toFixed(0):v.toFixed(2);}},nameTextStyle:{fontSize:10}},
            series:[{
                type:'scatter',data:data,
                symbolSize:function(val){return Math.min(25,Math.max(5,Math.log2(Math.max(2,val[2]))*3+3));},
                emphasis:{focus:'self',itemStyle:{borderColor:'#333',borderWidth:2},scale:1.3},
                label:{show:true,formatter:function(p){return p.data.tcName;},fontSize:8,position:'top',color:'#555'},
                labelLayout:{hideOverlap:true}
            }]
        },true);
    }

    function updateBoxplotChart(filtered){
        var sg={'1/3':[],'8':[],'9/10':[]};
        filtered.forEach(function(c){
            var l=c.loss||0; if(l<=0) return;
            if(c.signal<=3) sg['1/3'].push(l);
            else if(c.signal===8) sg['8'].push(l);
            else sg['9/10'].push(l);
        });
        var cats=[],boxData=[],outliers=[];
        ['1/3','8','9/10'].forEach(function(name){
            var a=sg[name]; if(a.length<1) return;
            a.sort(function(x,y){return x-y;});
            var n=a.length,q1=a[Math.floor(n*0.25)]||a[0],med=a[Math.floor(n*0.5)]||a[0],
                q3=a[Math.floor(n*0.75)]||a[n-1],iqr=q3-q1,
                lo=Math.max(a[0],q1-1.5*iqr),hi=Math.min(a[n-1],q3+1.5*iqr);
            var idx=cats.length;
            cats.push('Signal '+name);
            boxData.push([lo,q1,med,q3,hi]);
            a.filter(function(v){return v<lo||v>hi;}).forEach(function(v){outliers.push([idx,v]);});
        });
        boxplotChart.setOption({
            tooltip:{trigger:'item'},
            grid:{left:55,right:15,top:10,bottom:25},
            xAxis:{type:'category',data:cats,axisLabel:{fontSize:10}},
            yAxis:{type:'log',name:'Loss (HK$M)',min:0.01,axisLabel:{fontSize:10},nameTextStyle:{fontSize:10}},
            series:[
                {type:'boxplot',data:boxData,itemStyle:{color:'#d4e6f1',borderColor:'#1e3a5f'}},
                {type:'scatter',data:outliers,symbolSize:6,itemStyle:{color:'#e74c3c'}}
            ]
        },true);
    }

    function updateCasualtyChart(filtered){
        var yd={};
        filtered.forEach(function(c){
            if(!yd[c.year]) yd[c.year]={dead:0,injured:0,affected:0};
            yd[c.year].dead+=(c.dead||0);
            yd[c.year].injured+=(c.injured||0);
            yd[c.year].affected+=(c.affected||0);
        });
        var years=[];for(var y=yearRange[0];y<=yearRange[1];y++) years.push(y);
        casualtyChart.setOption({
            tooltip:{trigger:'axis'},
            legend:{data:['Deaths','Injuries','Affected (\u00F710)'],bottom:0,textStyle:{fontSize:10}},
            grid:{left:45,right:15,top:10,bottom:40},
            xAxis:{type:'category',data:years,axisLabel:{fontSize:10,rotate:45}},
            yAxis:{type:'value',name:'Count',nameTextStyle:{fontSize:10},axisLabel:{fontSize:10}},
            series:[
                {name:'Deaths',type:'bar',stack:'c',data:years.map(function(y){return(yd[y]||{}).dead||0;}),itemStyle:{color:'#e74c3c'},barMaxWidth:15},
                {name:'Injuries',type:'bar',stack:'c',data:years.map(function(y){return(yd[y]||{}).injured||0;}),itemStyle:{color:'#f39c12'},barMaxWidth:15},
                {name:'Affected (\u00F710)',type:'line',data:years.map(function(y){return Math.round(((yd[y]||{}).affected||0)/10);}),
                    itemStyle:{color:'#3498db'},lineStyle:{width:2},smooth:true,symbol:'circle',symbolSize:4}
            ]
        },true);
    }

    // ===== INIT =====
    function initTimeline(){
        var sl=document.getElementById('timeline-slider');
        noUiSlider.create(sl,{
            start:[1988,2023],connect:true,step:1,
            range:{'min':1988,'max':2023},
            format:{to:function(v){return Math.round(v);},from:function(v){return Number(v);}}
        });
        sl.noUiSlider.on('update',function(vals){
            yearRange=[parseInt(vals[0]),parseInt(vals[1])];
            document.getElementById('yearDisplay').innerText=yearRange[0]+' \u2013 '+yearRange[1];
        });
        sl.noUiSlider.on('change',function(){refreshAll();});
    }

    function initControls(){
        document.querySelectorAll('.btn-toggle[data-view]').forEach(function(btn){
            btn.addEventListener('click',function(){
                document.querySelectorAll('.btn-toggle[data-view]').forEach(function(b){b.classList.remove('active');});
                this.classList.add('active');
                currentView=this.dataset.view;
                renderMapView();
            });
        });
        document.getElementById('signalFilter').addEventListener('change',function(){
            signalFilter=this.value;
            refreshAll();
        });
        window.addEventListener('resize',function(){
            freqChart&&freqChart.resize();radarChart&&radarChart.resize();
            bubbleChart&&bubbleChart.resize();boxplotChart&&boxplotChart.resize();
            casualtyChart&&casualtyChart.resize();
            map.invalidateSize();
        });
    }

    window.onload=function(){
        initCharts();
        initTimeline();
        initControls();
        refreshAll();
    };
})();
<\/script>
</body>
</html>'''

# Replace placeholders with actual data
html = html.replace("CYCLONES_PLACEHOLDER", cyclones_json)
html = html.replace("WIND_PLACEHOLDER", wind_json)
html = html.replace("RAIN_PLACEHOLDER", rain_json)

with open('Interactive map.html', 'w', encoding='utf-8') as f:
    f.write(html)

import os
print(f"Written: {os.path.getsize('Interactive map.html')} bytes")
print("Done!")
