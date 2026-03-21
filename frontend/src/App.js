import React, { useState, useEffect } from 'react';
import './App.css';

const API_BASE = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

function App() {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [view, setView] = useState('home'); // 'home', 'manager', 'team_member'
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      fetchCurrentUser();
    } else {
      setLoading(false);
    }
  }, [token]);

  const fetchCurrentUser = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/auth/me`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const userData = await res.json();
        setUser(userData);
        setView(userData.role === 'manager' ? 'manager' : 'team_member');
      } else {
        localStorage.removeItem('token');
        setToken(null);
      }
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  const handleLogin = async (email, password) => {
    try {
      const res = await fetch(`${API_BASE}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      const data = await res.json();
      if (res.ok) {
        localStorage.setItem('token', data.access_token);
        setToken(data.access_token);
        setUser(data.user);
        setView(data.user.role === 'manager' ? 'manager' : 'team_member');
      } else {
        alert(data.detail || 'Login failed');
      }
    } catch (err) {
      console.error(err);
      alert('Login failed');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    setView('home');
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  if (!user) {
    return <LoginScreen onLogin={handleLogin} />;
  }

  if (view === 'home') {
    return <HomeScreen user={user} onNavigate={setView} onLogout={handleLogout} />;
  }

  if (view === 'manager') {
    return <ManagerDashboard user={user} token={token} onLogout={handleLogout} onNavigate={setView} />;
  }

  if (view === 'team_member') {
    return <TeamMemberDashboard user={user} token={token} onLogout={handleLogout} onNavigate={setView} />;
  }

  return null;
}

// Login Screen
function LoginScreen({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onLogin(email, password);
  };

  return (
    <div className="login-container">
      <div className="login-content">
        <div className="login-left">
          <div className="logo">P</div>
          <h1>PerformOS</h1>
          <h2>One-on-One Builder</h2>
          <p className="tagline">Better conversations. Safer teams. Stronger performance.</p>
        </div>
        <div className="login-right">
          <div className="login-form-container">
            <h3>Sign In</h3>
            <form onSubmit={handleSubmit} data-testid="login-form">
              <div className="form-group">
                <label>Email</label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="alex@performos.io"
                  required
                  data-testid="login-form-email-input"
                />
              </div>
              <div className="form-group">
                <label>Password</label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="demo"
                  required
                  data-testid="login-form-password-input"
                />
              </div>
              <button type="submit" className="btn-primary" data-testid="login-form-submit-button">
                Sign In
              </button>
            </form>
            <div className="demo-accounts">
              <p><strong>Demo Accounts</strong></p>
              <p className="small">Manager: alex@performos.io</p>
              <p className="small">Team Member: sarah@performos.io</p>
              <p className="small">Password for all: demo</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Home Screen
function HomeScreen({ user, onNavigate, onLogout }) {
  return (
    <div className="home-container">
      <div className="home-content">
        <div className="logo">P</div>
        <h1>PerformOS</h1>
        <h2>One-on-One Builder</h2>
        <p className="subtitle">Run structured performance conversations. Surface what matters. Protect your team.</p>

        <div className="role-cards">
          <div className="role-card" onClick={() => onNavigate('manager')} data-testid="role-select-manager-card">
            <div className="role-icon">📊</div>
            <h3>Manager View</h3>
            <p>Run one-on-ones, review history, see team health and risk flags</p>
            <button className="btn-secondary" data-testid="role-select-manager-continue-button">Open Dashboard →</button>
          </div>
          <div className="role-card" onClick={() => onNavigate('team_member')} data-testid="role-select-team-member-card">
            <div className="role-icon">💬</div>
            <h3>Team Member View</h3>
            <p>Complete pre-meeting reflections, view your own history</p>
            <button className="btn-secondary" data-testid="role-select-team-member-continue-button">Open Dashboard →</button>
          </div>
        </div>

        <div className="user-info">
          Signed in as {user.name} · <button onClick={onLogout} className="link-btn">Sign out</button>
        </div>
      </div>
    </div>
  );
}

// Manager Dashboard
function ManagerDashboard({ user, token, onLogout, onNavigate }) {
  const [activeTab, setActiveTab] = useState('schedule');
  const [members, setMembers] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [flags, setFlags] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [membersRes, sessionsRes, flagsRes, statsRes] = await Promise.all([
        fetch(`${API_BASE}/api/members`, { headers: { 'Authorization': `Bearer ${token}` } }),
        fetch(`${API_BASE}/api/sessions`, { headers: { 'Authorization': `Bearer ${token}` } }),
        fetch(`${API_BASE}/api/flags?status=open`, { headers: { 'Authorization': `Bearer ${token}` } }),
        fetch(`${API_BASE}/api/stats/dashboard`, { headers: { 'Authorization': `Bearer ${token}` } })
      ]);

      setMembers(await membersRes.json());
      setSessions(await sessionsRes.json());
      setFlags(await flagsRes.json());
      setStats(await statsRes.json());
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  const healthColor = (score) => {
    if (score >= 80) return '#10B981';
    if (score >= 60) return '#06B6D4';
    if (score >= 40) return '#F59E0B';
    return '#EF4444';
  };

  return (
    <div className="dashboard-container">
      <nav className="navbar">
        <div className="nav-content">
          <div className="nav-left">
            <span className="logo-small">P</span>
            <span className="nav-title">PerformOS · One-on-Ones</span>
          </div>
          <div className="nav-right">
            <span>{user.name}</span>
            <button onClick={() => onNavigate('home')} className="link-btn">← Home</button>
          </div>
        </div>
      </nav>

      <div className="dashboard-content">
        <div className="dashboard-header">
          <h1>Team One-on-Ones</h1>
          <p>Performance conversations and team health at a glance</p>
        </div>

        {stats && (
          <div className="metrics-grid">
            <div className="metric-card">
              <div className="metric-label">Upcoming This Week</div>
              <div className="metric-value">{stats.upcoming_sessions}</div>
              <div className="metric-icon">📅</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">Completed This Month</div>
              <div className="metric-value">{stats.completed_this_month}</div>
              <div className="metric-icon">✓</div>
            </div>
            <div className="metric-card metric-hero" style={{ borderColor: healthColor(stats.team_health_score) }}>
              <div className="metric-label">Team Health Score</div>
              <div className="metric-value" style={{ color: healthColor(stats.team_health_score) }}>{stats.team_health_score}</div>
              <div className="metric-icon">♡</div>
              <div className="health-bar">
                <div className="health-bar-fill" style={{ width: `${stats.team_health_score}%`, backgroundColor: healthColor(stats.team_health_score) }}></div>
              </div>
            </div>
            <div className="metric-card">
              <div className="metric-label">Active Flags</div>
              <div className="metric-value">{stats.active_flags}</div>
              <div className="metric-icon">⚑</div>
            </div>
          </div>
        )}

        <div className="tabs" data-testid="manager-dashboard-tabs">
          <button 
            className={activeTab === 'schedule' ? 'tab active' : 'tab'}
            onClick={() => setActiveTab('schedule')}
            data-testid="manager-dashboard-schedule-tab"
          >
            Schedule
          </button>
          <button 
            className={activeTab === 'team_health' ? 'tab active' : 'tab'}
            onClick={() => setActiveTab('team_health')}
            data-testid="manager-dashboard-team-health-tab"
          >
            Team Health ({flags.length})
          </button>
          <button 
            className={activeTab === 'performance' ? 'tab active' : 'tab'}
            onClick={() => setActiveTab('performance')}
            data-testid="manager-dashboard-performance-trends-tab"
          >
            Performance Trends
          </button>
        </div>

        {activeTab === 'schedule' && (
          <ScheduleTab members={members} sessions={sessions} flags={flags} />
        )}
        {activeTab === 'team_health' && (
          <TeamHealthTab members={members} sessions={sessions} flags={flags} />
        )}
        {activeTab === 'performance' && (
          <PerformanceTab members={members} sessions={sessions} />
        )}
      </div>
    </div>
  );
}

// Schedule Tab
function ScheduleTab({ members, sessions, flags }) {
  const getMemberFlags = (memberId) => flags.filter(f => f.member_id === memberId);
  
  const formatDate = (dateStr) => {
    if (!dateStr) return '—';
    const date = new Date(dateStr + 'T00:00:00');
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  };

  return (
    <div className="tab-content">
      <h3>Team Members</h3>
      <div className="members-list">
        {members.map(member => {
          const memberFlags = getMemberFlags(member._id);
          const memberSessions = sessions.filter(s => s.member_id === member._id);
          return (
            <div key={member._id} className="member-card">
              <div className="member-header">
                <div className="avatar">{member.avatar || member.name.split(' ').map(n => n[0]).join('')}</div>
                <div className="member-info">
                  <div className="member-name">{member.name}</div>
                  <div className="member-title">{member.title} · {member.cadence}</div>
                </div>
                {memberFlags.length > 0 && (
                  <div className="flag-badge">{memberFlags.length} flag{memberFlags.length !== 1 ? 's' : ''}</div>
                )}
              </div>
              <div className="member-details">
                <div className="detail-item">
                  <span className="label">Last session</span>
                  <span className="value">{formatDate(member.last_session)}</span>
                </div>
                <div className="detail-item">
                  <span className="label">Next</span>
                  <span className="value">{formatDate(member.next_session)}</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// Team Health Tab
function TeamHealthTab({ members, sessions, flags }) {
  const categoryLabel = {
    wellbeing: 'Wellbeing',
    psychological_safety: 'Psychological Safety',
    workload: 'Workload',
    engagement: 'Engagement',
    performance_confidence: 'Performance',
    team_dynamics: 'Team Dynamics',
    manager_gap: 'Manager Gap'
  };

  const severityLabel = {
    watch: 'Watch',
    concern: 'Concern',
    action_required: 'Action Required'
  };

  const severityClass = {
    watch: 'severity-watch',
    concern: 'severity-concern',
    action_required: 'severity-action'
  };

  const getMemberName = (memberId) => {
    const member = members.find(m => m._id === memberId);
    return member ? member.name : 'Unknown';
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return '—';
    const date = new Date(dateStr + 'T00:00:00');
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  return (
    <div className="tab-content">
      <h3>Active Flags ({flags.length})</h3>
      {flags.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">✓</div>
          <h4>No active risk flags</h4>
          <p>Your team is in a healthy place</p>
        </div>
      ) : (
        <div className="flags-list">
          {flags.map(flag => (
            <div key={flag._id} className={`flag-card ${severityClass[flag.severity]}`}>
              <div className="flag-header">
                <div className="flag-member">{getMemberName(flag.member_id)}</div>
                <div className={`flag-severity ${severityClass[flag.severity]}`}>
                  {severityLabel[flag.severity]}
                </div>
              </div>
              <div className="flag-category">{categoryLabel[flag.category]}</div>
              <div className="flag-signal">{flag.signal}</div>
              <div className="flag-date">Detected {formatDate(flag.created_at)}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// Performance Tab
function PerformanceTab({ members, sessions }) {
  const getMemberSessions = (memberId) => 
    sessions.filter(s => s.member_id === memberId && s.status === 'completed');

  const getAvgConfidence = (memberSessions) => {
    const scores = memberSessions
      .map(s => s.pre_meeting?.target_confidence)
      .filter(Boolean);
    if (scores.length === 0) return '—';
    return (scores.reduce((a, b) => a + b, 0) / scores.length).toFixed(1);
  };

  const getActionRate = (memberSessions) => {
    const allActions = memberSessions.flatMap(s => s.actions || []);
    if (allActions.length === 0) return '—';
    const completed = allActions.filter(a => a.status === 'completed').length;
    return Math.round((completed / allActions.length) * 100);
  };

  return (
    <div className="tab-content">
      <h3>Performance Overview</h3>
      <div className="performance-table">
        <table>
          <thead>
            <tr>
              <th>Team Member</th>
              <th>Sessions</th>
              <th>Avg Confidence</th>
              <th>Action Rate</th>
            </tr>
          </thead>
          <tbody>
            {members.map(member => {
              const memberSessions = getMemberSessions(member._id);
              const avgConf = getAvgConfidence(memberSessions);
              const actionRate = getActionRate(memberSessions);
              return (
                <tr key={member._id}>
                  <td>
                    <div className="member-name-cell">{member.name}</div>
                    <div className="member-title-cell">{member.title}</div>
                  </td>
                  <td>{memberSessions.length}</td>
                  <td>{avgConf}{avgConf !== '—' ? '/5' : ''}</td>
                  <td>{actionRate}{typeof actionRate === 'number' ? '%' : ''}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// Team Member Dashboard
function TeamMemberDashboard({ user, token, onLogout, onNavigate }) {
  const [member, setMember] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [membersRes, sessionsRes] = await Promise.all([
        fetch(`${API_BASE}/api/members`, { headers: { 'Authorization': `Bearer ${token}` } }),
        fetch(`${API_BASE}/api/sessions`, { headers: { 'Authorization': `Bearer ${token}` } })
      ]);

      const membersData = await membersRes.json();
      setMember(membersData[0]);
      setSessions(await sessionsRes.json());
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  const formatDate = (dateStr) => {
    if (!dateStr) return '—';
    const date = new Date(dateStr + 'T00:00:00');
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  };

  return (
    <div className="dashboard-container">
      <nav className="navbar">
        <div className="nav-content">
          <div className="nav-left">
            <span className="logo-small">P</span>
            <span className="nav-title">PerformOS · My One-on-Ones</span>
          </div>
          <div className="nav-right">
            <span>{user.name}</span>
            <button onClick={() => onNavigate('home')} className="link-btn">← Home</button>
          </div>
        </div>
      </nav>

      <div className="dashboard-content">
        <div className="dashboard-header">
          <h1>My One-on-Ones</h1>
          <p>Your reflections, goals, and development in one place</p>
        </div>

        <div className="tab-content">
          <div className="section-card">
            <h3>Upcoming Session</h3>
            {member && (
              <div className="upcoming-session">
                <p>Next one-on-one: {formatDate(member.next_session)}</p>
                <p className="small">Pre-meeting reflection will be available soon</p>
              </div>
            )}
          </div>

          <div className="section-card">
            <h3>Recent Sessions</h3>
            {sessions.length === 0 ? (
              <p className="empty-text">No sessions yet</p>
            ) : (
              <div className="sessions-list">
                {sessions.slice(0, 5).map(session => (
                  <div key={session._id} className="session-item">
                    <div className="session-date">{formatDate(session.date)}</div>
                    <div className="session-status">{session.status}</div>
                    {session.pre_meeting && (
                      <div className="session-scores">
                        <span>Confidence: {session.pre_meeting.target_confidence}/5</span>
                        <span>Feeling: {session.pre_meeting.feeling_about_work}/5</span>
                        <span>Workload: {session.pre_meeting.workload_manageable}/5</span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
