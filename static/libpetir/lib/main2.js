﻿/*! StormStation 5 NGX V1.1 ©2016 Astrogenic Systems  http://astrogenic.com No portion of this file may be copied, redistributed or modified without prior permission */
"use strict";

function StartApp2() {
    function e() {
        return function(e) {
            var t = e.getChildCount(),
                a = "lightning-cluster-",
                n = "background-color:rgba(63, 131, 238, 0.85); margin-left:8px";
            10 > t ? a += "low" : 100 > t ? (a += "medium", n = "background-color:rgba(207, 139, 16, 0.85); margin-left:5px") : (a += "high", n = 1e3 > t ? "background-color:rgba(255, 0, 0, 0.85); margin-left:2px" : "background-color:rgba(255, 0, 0, 0.85); margin-left:0px");
            var r = '<div class="cluster-label" style="' + n + '">' + t + "</div>";
            return L.divIcon({
                html: r,
                className: a,
                iconSize: L.point(32, 32)
            })
        }
    }
    map = new L.Map("map2", {
        center: new L.LatLng(appSettings.MapCenter.Lat, appSettings.MapCenter.Lon),
        zoom: 6,
        minZoom: 2,
        maxZoom: 18,
        zoomControl: !1
    }), purgeSchedTime = utl.epochTimestamp() + 6e4, recalcStatsSchedTime = utl.epochTimestamp() + 1e4, mStrikes = [], strikeRateCnt = new Counter(1), closeRateCnt = new Counter(1), allClearCnt = new Counter(5), CGPRateCnt = new Counter(1), CGNRateCnt = new Counter(1), ICRateCnt = new Counter(1), ("undefined" == appSettings.ClusteringMinZoom || null == appSettings.ClusteringMinZoom) && (appSettings.ClusteringMinZoom = 8), featureLayer = [], featureLayer[lyrCGF] = new L.markerClusterGroup({
        disableClusteringAtZoom: appSettings.ClusteringMinZoom,
        iconCreateFunction: e(),
        spiderfyOnMaxZoom: !0,
        chunkedLoading: !0,
        showCoverageOnHover: !1
    }), rangeRingsLayer = new L.featureGroup, map.addLayer(rangeRingsLayer), appSettings.MapProvider > mapProvider.length - 1 && (appSettings.MapProvider = 0), appSettings.MapProviderOverlay > mapProvider.length - 1 && (appSettings.MapProviderOverlay = -1), layer = mapProvider[appSettings.MapProvider], map.addLayer(layer), appSettings.MapProviderOverlay >= 0 && (mapFeatureLayer1 = mapProvider[appSettings.MapProviderOverlay], map.addLayer(mapFeatureLayer1)), map.addLayer(featureLayer[lyrCGF]), map.addControl(L.control.zoom({
        position: "bottomleft"
    })), map.on("zoomanim", debounce(map._onZoomTransitionEnd, 250)), ResetPanels2(), setInterval(UpdateGraphs2, 500), setInterval(GenMaint2, 500), SetPanelOpacity2(), SetRangeRings2(), ChangeHistory2(appSettings.StrikeHistoryMinutes), selectedTimeSpanMain = appSettings.GraphHistoryMinutes, ChangeSymbolSet2(appSettings.SymbolSet), map.setZoom(appSettings.InitialZoom), initDataLoad2()
}

function ResetPanels2() {
    0 == appSettings.ShowTypes ? (legendPanel = new LegendPanelNC, document.getElementById("pnlCanvas").setAttribute("height", "245"), document.getElementById("pnlSymCanvas").setAttribute("height", "37")) : legendPanel = new LegendPanel;
    var e = document.getElementById("map2").clientWidth - 250,
        t = document.getElementById("pnlCanvas").height + 10;
    document.getElementById("pnlCanvas").setAttribute("style", "z-index: 2; position:absolute; left:" + e + "px; top:5px;"), document.getElementById("pnlSymCanvas").setAttribute("style", "z-index: 2; position:absolute; left:" + e + "px; top:" + t + "px;"), clockCanvas = document.getElementById("pnlClockCanvas"), clockContext = clockCanvas.getContext("2d"), clockPanel.Create(clockCanvas, clockContext), clockPanel.Init(), clockPanel.StartTimeUpdate(), networkStatus = 0, errorStatus = 0, dataCanvas = document.getElementById("pnlCanvas"), dataContext = dataCanvas.getContext("2d"), dataPanel.Create(dataCanvas, dataContext), dataPanel.Init(), legendCanvas = document.getElementById("pnlSymCanvas"), legendContext = legendCanvas.getContext("2d"), legendPanel.Create(legendCanvas, legendContext), legendPanel.Init()
}

function SetRangeRings2() {
    var e = appSettings.FirstRing,
        t = appSettings.RingSpacing;
    "km" != appSettings.DistanceUnit && (e = utl.mi2Km(e), t = utl.mi2Km(t)), e *= 1e3, t *= 1e3, homeCenterPoint = new L.LatLng(appSettings.StationCenter.Lat, appSettings.StationCenter.Lon), numRangeRings = appSettings.NumRings, numRangeRings > 13 && (numRangeRings = 13), startDistMeters = e, spacingMeters = t, ringColor = appSettings.RingColor, drawRangeLabels = appSettings.DrawLabels, renderRangeRings2()
}

function renderRangeRings2() {
    if (rangeRingsLayer.clearLayers(), !(appSettings.NumRings < 1)) {
        L.marker(homeCenterPoint, {
            icon: centCrossIcon
        }).addTo(rangeRingsLayer);
        for (var e = startDistMeters, t = 0; numRangeRings > t; t++) {
            var a = L.geodesic([], {
                weight: 1,
                opacity: 1,
                color: ringColor,
                steps: 100
            }).addTo(rangeRingsLayer);
            if (a.createCircle(homeCenterPoint, e), drawRangeLabels) {
                var n = homeCenterPoint.destinationPoint(0, e / 1e3),
                    r = e / 1e3;
                "km" != appSettings.DistanceUnit && (r = utl.km2Mi(r));
                var o = L.divIcon({
                    className: "range-label",
                    html: r.toFixed(0).toString()
                });
                L.marker(n, {
                    icon: o
                }).addTo(rangeRingsLayer)
            }
            e += spacingMeters
        }
    }
}

function InjectData2(e) {
    var t = 0 == prevTimestamp,
        a = utl.epochTimestamp(),
        n = utl.epochTimestamp() - 6e4,
        r = JSON.parse(e);
    if (1 == appSettings.ShowTypes && "LD-250" == r.DetectorModel && (appSettings.ShowTypes = !1, ResetPanels2()), networkStatus = 1, dataPanel.SetNetworkStatus(networkStatus), SensorData.Lat = r.StationLat, SensorData.Lon = r.StationLon, SensorData.DecType = r.DetectorModel, SensorData.AntennaAlgn = r.AntennaAlignment, SensorData.NSVersion = r.SoftwareVersion, r.TimestampEpoch != prevTimestamp && 0 != r.StrikeData.length) {
        prevTimestamp = r.TimestampEpoch;
        for (var o = 0, i = 0; i < r.StrikeData.length; i++)
            if (!appSettings.HideUncorrelated || r.StrikeData[i].correlated) {
                var s = r.StrikeData[i].lat.toFixed(3).toString(),
                    l = r.StrikeData[i].lon.toFixed(3).toString();
                r.StrikeData[i].compoundType += 1, appSettings.ShowTypes || (r.StrikeData[i].compoundType = StrikeType.GEN);
                var p = r.StrikeData[i].compoundType,
                    m = r.StrikeData[i].millis,
                    d = new Date(m),
                    u = -1,
                    S = a - m;
                u = th05m > S ? flashIdxNew : th10m > S ? flashIdx10 : th20m > S ? flashIdx20 : th30m > S ? flashIdx30 : th40m > S ? flashIdx40 : th60m > S ? flashIdx50 : -1, u > 5 && (u = -1);
                var c = "",
                    C = GetSymbolByType2(StrikeType.GEN, u);
                p == StrikeType.CGP && (c = c = "Positive Cloud to Ground", C = GetSymbolByType2(StrikeType.CGP, u)), p == StrikeType.CGN ? (c = c = "Negative Cloud to Ground", C = GetSymbolByType2(StrikeType.CGN, u)) : p == StrikeType.ICF && (c = "Cloud Flash", C = GetSymbolByType2(StrikeType.ICF, u));
                var g = "km" == appSettings.DistanceUnit ? r.StrikeData[i].dist.toFixed(0) : utl.km2Mi(r.StrikeData[i].dist).toFixed(0),
                    y = "<span><font size=1>Time: <strong>" + utl.dtWithMillis(d.toLocaleString(), utl.padMS(d.getMilliseconds(), 3)) + "</strong><br>";
                y += "Position: <strong>" + s.toString() + "&deg;, " + l.toString() + "&deg;</strong><br>", y += "Bearing: <strong>" + parseFloat(r.StrikeData[i].bng).toFixed(1) + "°</strong> Distance: <strong>" + g + " " + appSettings.DistanceUnit + "</strong><br>", appSettings.ShowTypes && (y += "Type: <strong>" + c + "</strong><br>"), y += "</strong></font></span>", -1 != u && (r.StrikeData[i].marker = L.marker([s, l], {
                    icon: C,
                    zIndexOffset: 1e3
                }).bindPopup(y), mStrikes.push(r.StrikeData[i]), mStrikes[mStrikes.length - 1].marker.addTo(featureLayer[lyrCGF]), o++), 0 == t && (totRecord = [], totRecord.time = r.StrikeData[i].millis, totRecord.type = r.StrikeData[i].compoundType, totRecord.range = r.StrikeData[i].dist, totCounter.push(totRecord)), r.StrikeData[i].millis > n && (strikeRateCnt.increment(), p == StrikeType.CGP ? CGPRateCnt.increment() : p == StrikeType.CGN ? CGNRateCnt.increment() : p == StrikeType.ICF && ICRateCnt.increment())
            } o > 0 && dataPanel.SetFlash(1), t && (UpdateMarkersOptimized2(), RecalculateStats2()), dataPanel.UpdateCounters()
    }
}

function AddBufferData2(e) {
    if ("undefined" != e && null != e && 0 != e.length) {
        var t = utl.epochTimestamp(),
            a = utl.epochTimestamp() - 6e4,
            n = utl.epochTimestamp() - 60 * appSettings.GraphHistoryMinutes * 1e3,
            r = JSON.parse(e);
        r.StrikeData.sort(function(e, t) {
            e.millis - t.millis
        });
        var o = 0;
        for (r.StrikeData.length; r.StrikeData.length > 0 && r.StrikeData[0].Epoch < n;) r.StrikeData.shift(), o++;
        networkStatus = 1, dataPanel.SetNetworkStatus(networkStatus), "undefined" != r.StationLat && (SensorData.Lat = r.StationLat), "undefined" != r.StationLon && (SensorData.Lon = r.StationLon), "undefined" != r.DetectorModel && (SensorData.DecType = r.DetectorModel), "undefined" != r.AntennaAlignment && (SensorData.AntennaAlgn = r.AntennaAlignment), "undefined" != r.SoftwareVersion && (SensorData.NSVersion = r.SoftwareVersion), prevTimestamp = r.TimestampEpoch;
        for (var i = 0, s = 0; s < r.StrikeData.length; s++)
            if (!appSettings.HideUncorrelated || r.StrikeData[s].correlated) {
                var l = r.StrikeData[s].lat.toFixed(3).toString(),
                    p = r.StrikeData[s].lon.toFixed(3).toString();
                r.StrikeData[s].compoundType += 1, appSettings.ShowTypes || (r.StrikeData[s].compoundType = StrikeType.GEN);
                var m = r.StrikeData[s].compoundType,
                    d = r.StrikeData[s].millis,
                    u = new Date(d),
                    S = -1,
                    c = t - d;
                S = th05m > c ? flashIdxNew : th10m > c ? flashIdx10 : th20m > c ? flashIdx20 : th30m > c ? flashIdx30 : th40m > c ? flashIdx40 : th60m > c ? flashIdx50 : -1, S > 5 && (S = -1);
                var C = "",
                    g = GetSymbolByType2(StrikeType.GEN, S);
                m == StrikeType.CGP && (C = C = "Positive Cloud to Ground", g = GetSymbolByType2(StrikeType.CGP, S)), m == StrikeType.CGN ? (C = C = "Negative Cloud to Ground", g = GetSymbolByType2(StrikeType.CGN, S)) : m == StrikeType.ICF && (C = "Cloud Flash", g = GetSymbolByType2(StrikeType.ICF, S));
                var y = "km" == appSettings.DistanceUnit ? r.StrikeData[s].dist.toFixed(0) : utl.km2Mi(r.StrikeData[s].dist).toFixed(0),
                    k = "<span><font size=1 color = black>Time: <strong>" + utl.dtWithMillis(u.toLocaleString(), utl.padMS(u.getMilliseconds(), 3)) + "</strong><br>";
                k += "Position: <strong>" + l.toString() + "&deg;, " + p.toString() + "&deg;</strong><br>", k += "Bearing: <strong>" + parseFloat(r.StrikeData[s].bng).toFixed(1) + "°</strong> Distance: <strong>" + y + " " + appSettings.DistanceUnit + "</strong><br>", appSettings.ShowTypes && (k += "Type: <strong>" + C + "</strong><br>"), k += "</strong></font></span>", -1 != S && (r.StrikeData[s].marker = L.marker([l, p], {
                    icon: g,
                    zIndexOffset: 1e3
                }).bindPopup(k), mStrikes.push(r.StrikeData[s]), mStrikes[mStrikes.length - 1].marker.addTo(featureLayer[lyrCGF]), i++), totRecord = [], totRecord.time = r.StrikeData[s].millis, totRecord.type = r.StrikeData[s].compoundType, totRecord.range = r.StrikeData[s].dist, totCounter.push(totRecord), r.StrikeData[s].millis > a && (strikeRateCnt.increment(), m == StrikeType.CGP ? CGPRateCnt.increment() : m == StrikeType.CGN ? CGNRateCnt.increment() : m == StrikeType.ICF && ICRateCnt.increment())
            } UpdateMarkersOptimized2(), RecalculateStats2(), InsertGraphBuffers2(r), UpdateGraphBuffers2()
    }
}

function GenMaint2() {
    UpdateGraphBuffers2();
    var e = utl.epochTimestamp();
    if (e > purgeSchedTime) {
        purgeSchedTime = e + utl.min2millis(5);
        var t = 0,
            a = totCounter.length - 1;
        if (a >= 0) {
            var n = e - 432e5;
            do {
                if (!(totCounter[a].time < n)) break;
                totCounter.pop(), a = totCounter.length - 1, t++
            } while (a >= 0)
        }
    }
    e > recalcStatsSchedTime && (recalcStatsSchedTime = e + 1e4, RecalculateStats2())
}

function RecalculateStats2() {
    totalCount = 0, totalCountCGP = 0, totalCountCGN = 0, totalCountICF = 0, totalCountClose = 0;
    for (var e = utl.epochTimestamp() - utl.min2millis(selectedTimeSpanMain), t = 0; t < totCounter.length; t++) totCounter[t].time < e || (totCounter[t].type == StrikeType.CGP ? totalCountCGP++ : totCounter[t].type == StrikeType.CGN ? totalCountCGN++ : totCounter[t].type == StrikeType.ICF && totalCountICF++, totCounter[t].range < alarmRange && totalCountClose++);
    totalCount = totalCountCGP + totalCountCGN + totalCountICF, pctCGP = 0, pctCGN = 0, pctICF = 0, pctClose = 0, totalCount > 0 && (pctCGP = Math.round(totalCountCGP / totalCount * 100), pctCGN = Math.round(totalCountCGN / totalCount * 100), pctICF = Math.round(totalCountICF / totalCount * 100), pctClose = Math.round(totalCountClose / totalCount * 100))
}

function InsertGraphBuffers2(e) {
    for (var t = 0, a = 0; a < e.StrikeData.length; a++) {
        var n = new Date(e.StrikeData[a].millis),
            r = 60 * n.getHours() + n.getMinutes();
        e.StrikeData[a].compoundType == StrikeType.CGP ? (++srBufCGP[r], t++) : e.StrikeData[a].compoundType == StrikeType.CGN || e.StrikeData[a].compoundType == StrikeType.GEN ? (++srBufCGN[r], t++) : e.StrikeData[a].compoundType == StrikeType.ICF && (++srBufICF[r], t++), appSettings.ShowTypes || e.StrikeData[a].compoundType != StrikeType.GEN || (++srBufCGN[r], t++), srBufTotal[r] = srBufCGP[r] + srBufCGN[r] + srBufICF[r]
    }
}

function UpdateGraphBuffers2() {
    var e = utl.timestampMin(),
        t = 0;
    appSettings.ShowTypes ? (t = CGPRateCnt.currentCount(), t > srBufCGP[e] && (srBufCGP[e] = t), t = CGNRateCnt.currentCount(), t > srBufCGN[e] && (srBufCGN[e] = t), t = ICRateCnt.currentCount(), t > srBufICF[e] && (srBufICF[e] = t), srBufTotal[e] = srBufCGP[e] + srBufCGN[e] + srBufICF[e]) : (t = strikeRateCnt.currentCount(), t > srBufTotal[e] && (srBufTotal[e] = t)), t = closeRateCnt.currentCount(), t > srBufClose[e] && (srBufClose[e] = t), bufPointer = e, e = utl.timestampMinNext(), srBufCGP[e] = 0, srBufCGN[e] = 0, srBufICF[e] = 0, srBufClose[e] = 0, srBufTotal[e] = 0
}

function UpdateGraphs2() {
    dataPanel.UpdateCounters()
}

function UpdateMarkersOptimized2() {
    var e = utl.epochTimestamp();
    for (featureLayer[lyrCGF].clearLayers(), mStrikes.sort(function(e, t) {
            return parseInt(e.millis) - parseInt(t.millis)
        }); mStrikes.length > 3e3;) mStrikes.shift();
    for (var t = 0; t < mStrikes.length; t++) {
        var a = e - mStrikes[t].millis;
        a >= th60m ? mStrikes.shift() : (a <= StrokeAgeMS.M5 ? mStrikes[t].marker.setIcon(GetSymbolByType2(mStrikes[t].compoundType, flashIdxNew)) : a <= StrokeAgeMS.M10 ? mStrikes[t].marker.setIcon(GetSymbolByType2(mStrikes[t].compoundType, flashIdx10)) : a <= StrokeAgeMS.M20 ? mStrikes[t].marker.setIcon(GetSymbolByType2(mStrikes[t].compoundType, flashIdx20)) : a <= StrokeAgeMS.M30 ? mStrikes[t].marker.setIcon(GetSymbolByType2(mStrikes[t].compoundType, flashIdx30)) : a <= StrokeAgeMS.M40 ? mStrikes[t].marker.setIcon(GetSymbolByType2(mStrikes[t].compoundType, flashIdx40)) : a <= StrokeAgeMS.M60 && mStrikes[t].marker.setIcon(GetSymbolByType2(mStrikes[t].compoundType, flashIdx50)), a <= StrokeAgeMS.M60 && featureLayer[lyrCGF].addLayer(mStrikes[t].marker))
    }
    clearTimeout(tmrUpdateMapId), tmrUpdateMapId = setTimeout(UpdateMarkersOptimized2, 6e4)
}

function GetSymbolByType2(e, t) {
    if (!(0 > t || t > 5)) {
        var a = currentSymSet;
        return 0 == appSettings.ShowTypes && (e = 2), 1 == e ? cgpStrikeSym[a + t] : 2 == e ? cgnStrikeSym[a + t] : icFlashSym[a + t]
    }
}

function ChangeHistory2(e) {
    if (selectedHistory != e) {
        selectedHistory = e;
        var t = 1;
        30 == selectedHistory ? t = .5 : 15 == selectedHistory ? t = .25 : 6 == selectedHistory && (t = .1), StrokeAgeMS = {
            M5: th05m * t,
            M10: th10m * t,
            M20: th20m * t,
            M30: th30m * t,
            M40: th40m * t,
            M50: th50m * t,
            M60: th60m * t
        }, StrokeAgeMIN = {
            M5: 5 * t,
            M10: 10 * t,
            M20: 20 * t,
            M30: 30 * t,
            M40: 40 * t,
            M50: 50 * t,
            M60: 60 * t
        }, UpdateMarkersOptimized2(), legendPanel.Init()
    }
}

function ChangeSymbolSet2(e) {
    6 * e != currentSymSet && (currentSymSet = 6 * e, UpdateMarkersOptimized2(), legendPanel.Init())
}

function _extCall_SetNEXRADOpacity2() {
    radarOpacity = arguments[0], null != radar && radar.setOpacity(radarOpacity)
}

function SetPanelOpacity2() {
    panelOpacity = appSettings.PanelOpacity, pnlBg = "rgba(30, 30, 30, " + panelOpacity + ")", dataPanel.Init(), clockPanel.Init(), legendPanel.Init()
}

function initDataLoad2() {
    timer = setInterval(loadRealtimeData2, 4e3), loadRetryCount = 0, loadBufferedData(), loadRealtimeData2()
}

function loadRealtimeData2() {
    errorStatus = 0, networkStatus = 0, xhr = new XMLHttpRequest, xhr.onreadystatechange = realtimeLoad, xhr.open("GET", appSettings.DataFileRelativePath + "ngxdata.json?" + (new Date).getTime(), !0), xhr.responseType = "application/json", xhr.send()
}

function loadBufferedData() {
    xhrBuf = new XMLHttpRequest, xhrBuf.onreadystatechange = bufferLoad, xhrBuf.open("GET", appSettings.DataFileRelativePath + "ngxarchive.json?" + (new Date).getTime(), !0), xhrBuf.responseType = "application/json", xhrBuf.send()
}

function realtimeLoad() {
    if (4 == xhr.readyState && 200 == xhr.status) {
        JSON.parse(xhr.responseText);
        debounce(InjectData2(xhr.responseText), 250), loadRetryCount = 0, clearInterval(timer), timer = setInterval(loadRealtimeData2, 4e3)
    } else 4 == xhr.readyState && 404 == xhr.status && (loadRetryCount++ < 3 ? (clearInterval(timer), timer = setInterval(loadRealtimeData2, 1e3)) : (errorStatus = 1, dataPanel.SetErrorStatus(errorStatus), loadRetryCount = 0, clearInterval(timer), timer = setInterval(loadRealtimeData2, 3e3)))
}

function bufferLoad() {
    if (4 == xhrBuf.readyState && 200 == xhrBuf.status) {
        JSON.parse(xhrBuf.responseText);
        AddBufferData2(xhrBuf.responseText)
    }
}

function loadSettings() {
    var e = new XMLHttpRequest;
    e.overrideMimeType("application/json"), e.onreadystatechange = function() {
        4 == e.readyState && 200 == e.status && (appSettings = JSON.parse(e.responseText), utl.endsWith(appSettings.DataFileRelativePath, "/") || (appSettings.DataFileRelativePath += "/"), console.log("Settings loaded"), StartApp2())
    }, e.open("GET", "static/libpetir/options/settings.json?" + (new Date).getTime(), !0), e.responseType = "application/json", e.send()
}

function debounce(e, t, a) {
    var n;
    return function() {
        var r = this,
            o = arguments,
            i = function() {
                n = null, a || e.apply(r, o)
            },
            s = a && !n;
        clearTimeout(n), n = setTimeout(i, t), s && e.apply(r, o)
    }
}
var utl = new UtilClass,
    appSettings;
preloadImages(loadSettings);
var centCrossIcon = L.icon({
        iconUrl: centCross.src,
        iconSize: [21, 21],
        iconAnchor: [10, 10]
    }),
    playAlarm = !0,
    playClick = !0,
    closeSymSet = !0,
    lyrCGF = 0,
    lyrCGP = 1,
    lyrCGN = 2,
    lyrICF = 3,
    StrikeType = Object.freeze({
        GEN: 0,
        CGP: 1,
        CGN: 2,
        ICF: 3,
        CGPF: 4,
        CGNF: 5
    }),
    StrikeCol = Object.freeze({
        CGP: "red",
        CGN: "gold",
        ICF: "deepskyblue",
        GEN: "orange",
        SUM: "white",
        IND: "lime",
        IND_ERR: "red",
        IND_WRN: "yellow"
    }),
    GraphTimeSpan = Object.freeze({
        H0: 30,
        H1: 60,
        H2: 120,
        H4: 240,
        H8: 480,
        H12: 720
    }),
    tmrUpdateMapId, th05m = 3e5,
    th10m = 6e5,
    th20m = 12e5,
    th30m = 18e5,
    th40m = 24e5,
    th50m = 3e6,
    th60m = 36e5,
    selectedHistory = 60,
    StrokeAgeMS = {
        M5: 3e5,
        M10: 6e5,
        M20: 12e5,
        M30: 18e5,
        M40: 24e5,
        M50: 3e6,
        M60: 36e5
    },
    StrokeAgeMIN = {
        M5: 5,
        M10: 10,
        M20: 20,
        M30: 30,
        M40: 40,
        M50: 50,
        M60: 60
    },
    selectedTimeSpanClose = GraphTimeSpan.H1,
    selectedTimeSpanMain = GraphTimeSpan.H1,
    panelOpacity = .7,
    radarOpacity = .6,
    pnlBg = "rgba(30, 30, 30, " + panelOpacity + ")",
    timerId, showRadar = !0,
    radar, numRangeRings, startDistMeters, spacingMeters, drawRangeRings, drawRangeLabels, ringColor, alarmRingColor, homeCenterPoint, alarmRange, alarmActive = !1,
    alarmDrawRing = !0,
    alarmDrawLabel = !0,
    emailAlertsActive = !1,
    networkStatus = 0,
    errorStatus = 0,
    hasSystemMessage = !1,
    nearStrokeData = [];
nearStrokeData.dist = 9999999, nearStrokeData.distMi = 9999999, nearStrokeData.bng = -1, nearStrokeData.time = -1;
var currZoomLevel, prevZoomLevel = -1,
    ZoomType = Object.freeze({
        CLOSE: 0,
        FAR: 1
    }),
    currZoomType, totRecord = [];
totRecord.time = 0, totRecord.type = 0, totRecord.range = 0;
for (var totCounter = [], purgeSchedTime = 0, recalcStatsSchedTime = 0, totalCount = 0, totalCountCGP = 0, totalCountCGN = 0, totalCountICF = 0, totalCountClose = 0, pctCGP = 0, pctCGN = 0, pctICF = 0, pctClose = 0, srBufCGP = [], srBufCGN = [], srBufICF = [], srBufClose = [], srBufTotal = [], bufPointer = 0, i = 0; 1440 > i; i++) srBufCGP[i] = 0, srBufCGN[i] = 0, srBufICF[i] = 0, srBufClose[i] = 0, srBufTotal[i] = 0;
var closeAlarmTriggered = !1,
    closeAlarmMuted = !1,
    caTimerId, dataPanel = new DataPanel,
    dataCanvas, dataContext, clockPanel = new ClockPanel,
    clockCanvas, clockContext, sym = new Symbols;
sym.Create();
var legendPanel, legendCanvas, legendContext, SensorData = {
        Lat: 0,
        Lon: 0,
        DecType: "Unknown",
        NSVersion: "0.0.0.0",
        AntennaAlgn: 0
    },
    map, mStrikes, strikeRateCnt, closeRateCnt, allClearCnt, CGPRateCnt, CGNRateCnt, ICRateCnt, featureLayer, rangeRingsLayer, layer, currentLayer = 0,
    currentSymSet = 0,
    mapFeatureLayer1, internalTimestamp = 0,
    prevTimestamp = 0,
    timer, loadRetryCount, xhr, xhrBuf;