import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  CircleMarker,
  MapContainer,
  Popup,
  TileLayer,
  useMap,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import "./styles.css";
import "./map.css";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const intelligence = [
  [
    "amnesia",
    "Infrastructure amnesia",
    "Repairs followed by another failure in under 90 days.",
  ],
  ["echo", "Failure echo mapper", "Related failures on nearby city assets."],
  [
    "signature",
    "Failure signature",
    "Repeated contributing factors in failure records.",
  ],
  [
    "comparison",
    "Intervention comparison",
    "Which historic repair held up best.",
  ],
  ["survival", "Repair survival", "Time from repair to the next failure."],
  [
    "planner",
    "Preventive action planner",
    "Priority score and recommended action.",
  ],
];

function api(path) {
  return fetch(`${API_BASE}${path}`).then(async (response) => {
    const data = await response.json().catch(() => null);
    if (!response.ok)
      throw new Error(data?.detail || `Request failed (${response.status})`);
    if (data?.message) throw new Error(data.message);
    return data;
  });
}

const label = (value) => (value == null || value === "" ? "—" : value);
const date = (value) =>
  value
    ? new Intl.DateTimeFormat("en-IN", {
        day: "2-digit",
        month: "short",
        year: "numeric",
      }).format(new Date(`${value}T00:00:00`))
    : "—";

function Empty({ children = "No patterns were detected for this asset." }) {
  return (
    <div className="empty">
      <span aria-hidden="true">—</span>
      {children}
    </div>
  );
}

function MapBounds({ assets }) {
  const map = useMap();
  useEffect(() => {
    if (assets.length === 1)
      map.setView([assets[0].latitude, assets[0].longitude], 14);
    if (assets.length > 1)
      map.fitBounds(
        assets.map((asset) => [asset.latitude, asset.longitude]),
        { padding: [35, 35] },
      );
  }, [assets, map]);
  return null;
}

function Map({ assets, selectedId, onSelect }) {
  const valid = assets.filter(
    (asset) =>
      Number.isFinite(Number(asset.latitude)) &&
      Number.isFinite(Number(asset.longitude)),
  );
  if (!valid.length)
    return (
      <div className="map empty">
        No location data is available for these assets.
      </div>
    );
  return (
    <div className="map" aria-label="Asset location map">
      <div className="map-label">Asset locations</div>
      <div className="map-key">
        <i /> Selected asset
      </div>
      <MapContainer
        center={[valid[0].latitude, valid[0].longitude]}
        zoom={13}
        scrollWheelZoom
        className="leaflet-map"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <MapBounds assets={valid} />
        {valid.map((asset) => (
          <CircleMarker
            key={asset.id}
            center={[asset.latitude, asset.longitude]}
            radius={asset.id === selectedId ? 10 : 7}
            pathOptions={{
              color: asset.id === selectedId ? "#a34334" : "#176351",
              fillColor: asset.id === selectedId ? "#c65745" : "#25836d",
              fillOpacity: 0.9,
              weight: 2,
            }}
            eventHandlers={{ click: () => onSelect(asset) }}
          >
            <Popup>
              <strong>{asset.asset_code}</strong>
              <br />
              {asset.asset_type}
              <br />
              {asset.condition} condition · {asset.importance} importance
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>
    </div>
  );
}

function Timeline({ history }) {
  if (!history?.length)
    return <Empty>No events have been recorded for this asset.</Empty>;
  return (
    <ol className="timeline">
      {history.map((event, index) => (
        <li
          key={event.id ?? index}
          className={
            event.event_type === "Failure" ? "failure" : "intervention"
          }
        >
          <div className="timeline-date">{date(event.event_date)}</div>
          <div>
            <span className="event-kind">{event.event_type}</span>
            <p>{label(event.description)}</p>
            {event.outcome && <small>Outcome: {event.outcome}</small>}
          </div>
        </li>
      ))}
    </ol>
  );
}

function IntelligenceContent({ kind, data }) {
  if (data == null || typeof data !== "object") {
    return <Empty>Intelligence data is not available for this asset.</Empty>;
  }
  if (Array.isArray(data) && data.length === 0) return <Empty />;
  if (kind === "planner") {
    if (Array.isArray(data)) return <Empty>No preventive plan is available.</Empty>;
    return (
      <div className="planner">
        <div
          className="score"
          style={{
            "--score": `${Math.min(100, Number(data.priority_score) || 0)}%`,
          }}
        >
          <b>{label(data.priority_score)}</b>
          <span>/100</span>
        </div>
        <div>
          <strong>{label(data.priority)} priority</strong>
          <p>{label(data.recommended_action)}</p>
          <small>
            {label(data.failure_count)} failures ·{" "}
            {label(data.intervention_count)} interventions
          </small>
        </div>
      </div>
    );
  }
  if (kind === "signature")
    return !data?.patterns?.length ? (
      <Empty />
    ) : (
      <div className="pattern-list">
        {data.patterns.map((item, i) => (
          <div key={i}>
            <strong>{item.factor}</strong>
            <span>{item.failure_occurrences} occurrences</span>
            <p>{item.interpretation}</p>
          </div>
        ))}
      </div>
    );
  if (kind === "comparison")
    return !data?.historical_results?.length ? (
      <Empty>No comparable intervention history is available.</Empty>
    ) : (
      <>
        <div className="bar-list">
          {data.historical_results.map((item, i) => (
            <div key={i}>
              <span title={item.intervention}>
                {date(item.intervention_date)}
              </span>
              <div>
                <i
                  style={{
                    width: `${Math.min(100, Number(item.survival_days) || 0)}%`,
                  }}
                />
              </div>
              <b>{item.survival_days} d</b>
            </div>
          ))}
        </div>
        {data.historically_better_intervention && (
          <p className="insight">
            Best historic result:{" "}
            {data.historically_better_intervention.survival_days} days.
          </p>
        )}
      </>
    );
  if (kind === "survival") {
    if (!Array.isArray(data) || data.length === 0) {
      return (
        <Empty>No repair-survival records are available for this asset.</Empty>
      );
    }

    return (
      <div className="bar-list">
        {data.map((item, i) => (
          <div key={i}>
            <span>{date(item.intervention_date)}</span>
            <div>
              <i
                style={{
                  width: `${Math.min(100, Number(item.survival_days) || 0)}%`,
                }}
              />
            </div>
            <b>{item.survival_days} d</b>
          </div>
        ))}
      </div>
    );
  }
  if (!Array.isArray(data) || data.length === 0) {
    return (
      <Empty>
        No linked incidents or repeat-repair patterns were detected.
      </Empty>
    );
  }

  return (
    <div className="record-list">
      {data.map((item, i) => (
        <div key={i}>
          <strong>{item.reason || item.asset_code || "Linked incident"}</strong>
          <p>
            {Object.entries(item)
              .filter(([key]) => !["reason", "id"].includes(key))
              .map(([key, value]) => `${key.replaceAll("_", " ")}: ${value}`)
              .join(" · ")}
          </p>
        </div>
      ))}
    </div>
  );
}

function IntelligenceCard({ kind, title, description, result }) {
  // Signals are requested after an asset is selected. Defaulting to loading
  // prevents the initial render from trying to display undefined API data.
  const { loading = true, data, error } = result || {};
  return (
    <section className="intel-card">
      <header>
        <div>
          <h3>{title}</h3>
          <p>{description}</p>
        </div>
        <span className={`status ${error ? "issue" : ""}`}>
          {loading ? "Checking" : error ? "Unavailable" : "Ready"}
        </span>
      </header>
      {loading ? (
        <div className="loading-lines">
          <i />
          <i />
          <i />
        </div>
      ) : error ? (
        <div className="error-note">
          {error === "Asset not found"
            ? "This asset is no longer available."
            : "Couldn’t load this intelligence signal."}
        </div>
      ) : (
        <IntelligenceContent kind={kind} data={data} />
      )}
    </section>
  );
}

function App() {
  const [assets, setAssets] = useState([]);
  const [selected, setSelected] = useState(null);
  const [assetState, setAssetState] = useState({ loading: true });
  const [details, setDetails] = useState(null);
  const [signals, setSignals] = useState({});
  const [query, setQuery] = useState("");
  useEffect(() => {
    api("/assets/")
      .then((data) => {
        setAssets(Array.isArray(data) ? data : []);
        setSelected(data?.[0] ?? null);
        setAssetState({});
      })
      .catch((e) => setAssetState({ error: e.message }));
  }, []);
  useEffect(() => {
    if (!selected) return;
    let alive = true;
    setDetails({ loading: true });
    setSignals(
      Object.fromEntries(
        intelligence.map(([kind]) => [kind, { loading: true }]),
      ),
    );
    api(`/events/${selected.id}`)
      .then((data) => alive && setDetails({ data }))
      .catch((e) => alive && setDetails({ error: e.message }));
    intelligence.forEach(([kind]) =>
      api(`/events/${kind}/${selected.id}`)
        .then(
          (data) =>
            alive && setSignals((prev) => ({ ...prev, [kind]: { data } })),
        )
        .catch(
          (e) =>
            alive &&
            setSignals((prev) => ({ ...prev, [kind]: { error: e.message } })),
        ),
    );
    return () => {
      alive = false;
    };
  }, [selected?.id]);
  const filtered = assets.filter((a) =>
    `${a.asset_code} ${a.asset_type} ${a.condition} ${a.importance}`
      .toLowerCase()
      .includes(query.toLowerCase()),
  );
  const select = (asset) => {
    setSelected(asset);
    document
      .getElementById("asset-detail")
      ?.scrollIntoView({ behavior: "smooth", block: "start" });
  };
  return (
    <div className="app">
      <aside>
        <div className="brand">
          <span>CM</span>
          <div>
            CITYMEMORY<small>Infrastructure intelligence</small>
          </div>
        </div>
        <nav>
          <a className="active" href="#overview">
            Overview
          </a>
          <a href="#asset-detail">Asset intelligence</a>
        </nav>
        <div className="sidebar-note">
          <b>Live city register</b>
          <span>Data source: FastAPI</span>
          <code>{API_BASE}</code>
        </div>
      </aside>
      <main>
        <header className="topbar">
          <div>
            <p className="eyebrow">Operations dashboard</p>
            <h1>City infrastructure</h1>
          </div>
          <div className="connection">
            <i className={assetState.error ? "offline" : ""} />
            {assetState.error ? "API unavailable" : "Live connection"}
          </div>
        </header>
        <section id="overview" className="overview">
          <div className="section-title">
            <div>
              <h2>Asset register</h2>
              <p>
                Monitor condition, criticality and field history in one view.
              </p>
            </div>
            <div className="metric">
              <b>{assets.length}</b> tracked assets
            </div>
          </div>
          <div className="overview-grid">
            <div className="asset-panel">
              <label className="search">
                <span>⌕</span>
                <input
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Search asset code, type or condition"
                />
              </label>
              {assetState.loading ? (
                <div className="center">Loading asset register…</div>
              ) : assetState.error ? (
                <div className="center error-note">
                  Unable to reach the local API. Start the FastAPI server at
                  port 8000.
                </div>
              ) : (
                <div className="asset-table">
                  <div className="table-head">
                    <span>Asset</span>
                    <span>Condition</span>
                    <span>Priority</span>
                  </div>
                  {filtered.map((asset) => (
                    <button
                      className={`asset-row ${asset.id === selected?.id ? "current" : ""}`}
                      key={asset.id}
                      onClick={() => select(asset)}
                    >
                      <span>
                        <b>{asset.asset_code}</b>
                        <small>
                          {asset.asset_type} · {asset.latitude},{" "}
                          {asset.longitude}
                        </small>
                      </span>
                      <span
                        className={`condition ${String(asset.condition).toLowerCase()}`}
                      >
                        {asset.condition}
                      </span>
                      <span>{asset.importance}</span>
                    </button>
                  ))}
                  {!filtered.length && (
                    <Empty>No assets match this search.</Empty>
                  )}
                </div>
              )}
            </div>
            <Map
              assets={filtered}
              selectedId={selected?.id}
              onSelect={select}
            />
          </div>
        </section>
        <section id="asset-detail" className="detail">
          {!selected ? (
            <div className="center">
              Select an asset to inspect its history.
            </div>
          ) : (
            <>
              <div className="asset-heading">
                <div>
                  <a href="#overview">← Back to assets</a>
                  <h2>
                    {selected.asset_code}
                    <span>{selected.asset_type}</span>
                  </h2>
                  <p>
                    {selected.latitude}, {selected.longitude} · Installed{" "}
                    {date(selected.installation_date)}
                  </p>
                </div>
                <div className="asset-facts">
                  <div>
                    <span>Condition</span>
                    <b>{details?.data?.condition ?? selected.condition}</b>
                  </div>
                  <div>
                    <span>Importance</span>
                    <b>{details?.data?.importance ?? selected.importance}</b>
                  </div>
                </div>
              </div>
              <div className="detail-grid">
                <section className="history">
                  <header>
                    <div>
                      <h2>Maintenance history</h2>
                      <p>Failures and interventions in chronological order.</p>
                    </div>
                  </header>
                  {details?.loading ? (
                    <div className="center">Loading history…</div>
                  ) : details?.error ? (
                    <div className="error-note">
                      {details.error === "Asset not found"
                        ? "This asset is no longer available."
                        : "Couldn’t load the event history."}
                    </div>
                  ) : (
                    <Timeline history={details?.data?.history} />
                  )}
                </section>
                <section className="signals">
                  <div className="signals-heading">
                    <h2>Intelligence signals</h2>
                    <p>Evidence derived from this asset’s recorded history.</p>
                  </div>
                  <div className="signals-grid">
                    {intelligence.map(([kind, title, description]) => (
                      <IntelligenceCard
                        key={kind}
                        kind={kind}
                        title={title}
                        description={description}
                        result={signals[kind]}
                      />
                    ))}
                  </div>
                </section>
              </div>
            </>
          )}
        </section>
      </main>
    </div>
  );
}

createRoot(document.getElementById("root")).render(<App />);
