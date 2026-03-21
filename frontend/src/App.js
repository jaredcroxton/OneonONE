import React, { useState, useEffect } from 'react';
import './App.css';

const API_BASE = process.env.REACT_APP_BACKEND_URL || '';
const CURRENT_WEEK = '2026-03-23';

// Utility functions
const getAvatarColor = (name) => {
  const colors = ['#3B82F6', '#06B6D4', '#10B981', '#8B5CF6', '#F59E0B', '#EC4899'];
  return colors[name.length % colors.length];
};

const getScoreColor = (rating) => {
  if (rating >= 4) return '#10B981';
  if (rating === 3) return '#06B6D4';
  return '#F59E0B';
};

const formatDate = (dateStr) => {
  if (!dateStr) return '—';
  const date = new Date(dateStr + 'T00:00:00');
  return date.toLocaleDateString('en-AU', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' });
};

const formatDateShort = (dateStr) => {
  if (!dateStr) return '—';
  const date = new Date(dateStr + 'T00:00:00');
  return date.toLocaleDateString('en-AU', { day: 'numeric', month: 'short' });
};

// API helper
const apiCall = async (endpoint, options = {}) => {
  const token = localStorage.getItem('token');
  const headers = {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` }),
    ...options.headers
  };

  const res = await fetch(`${API_BASE}${endpoint}`, { ...options, headers });
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(error.detail || 'Request failed');
  }
  return res.json();
};

// QUESTIONS DEFINITION
const QUESTIONS = [
  { id: 'proud_of', section: 'performance', label: "What's the result you're most proud of since our last one-on-one?", ratingLabel: 'How proud do you feel?', low: 'Not very', high: 'Extremely proud' },
  { id: 'stuck_on', section: 'performance', label: 'Where are you stuck or behind on your goals?', ratingLabel: 'How blocked do you feel?', low: 'Not blocked', high: 'Completely stuck' },
  { id: 'need_from_manager', section: 'performance', label: 'What do you need from me to move forward?', ratingLabel: 'How urgent is this support?', low: 'Not urgent', high: 'Critical' },
  { id: 'target_confidence', section: 'performance', label: 'Rate your confidence in hitting your current targets', ratingLabel: 'Confidence level', low: 'Low confidence', high: 'Very confident' },
  { id: 'feeling_about_work', section: 'wellbeing', label: 'How are you feeling about work right now?', ratingLabel: 'Overall feeling', low: 'Struggling', high: 'Thriving' },
  { id: 'safe_to_raise_concerns', section: 'wellbeing', label: 'Do you feel safe raising concerns or disagreeing with decisions in our team?', ratingLabel: 'Psychological safety', low: 'Not at all', high: 'Completely safe' },
  { id: 'feel_supported', section: 'wellbeing', label: 'How supported do you feel by your team?', ratingLabel: 'Support level', low: 'Not supported', high: 'Very supported' },
  { id: 'workload_manageable', section: 'wellbeing', label: 'Is your workload manageable right now?', ratingLabel: 'Workload level', low: 'Overwhelmed', high: 'Comfortable' },
  { id: 'anything_affecting', section: 'wellbeing', label: "Is there anything affecting your work that you'd like to talk about?", ratingLabel: 'How much is this impacting you?', low: 'Minimal impact', high: 'Significant impact', optional: true }
];

// COMPONENTS
function Avatar({ name, size = 52, healthStatus }) {
  const initials = name.split(' ').map(n => n[0]).join('');
  const color = getAvatarColor(name);

  return (
    <div className="avatar" style={{ width: size, height: size, background: color }}>
      {initials}
      {healthStatus && <div className={`health-dot ${healthStatus}`}></div>}
    </div>
  );
}

function RatingCommentInput({ question, value, onChange }) {
  const v = value || { rating: 0, comment: '' };

  return (
    <div className="question-group">
      <div className="question-label">
        {question.label}
        {question.optional && <span className="optional">(optional)</span>}
      </div>
      
      <div className="rating-row">
        <span className="rating-label">{question.ratingLabel}</span>
        <span className="rating-hint">{question.low}</span>
        <div className="rating-scale">
          {[1, 2, 3, 4, 5].map(n => (
            <button
              key={n}
              type="button"
              className={`rating-btn ${v.rating === n ? 'selected' : ''}`}
              onClick={() => onChange({ ...v, rating: n })}
            >
              {n}
            </button>
          ))}
        </div>
        <span className="rating-hint">{question.high}</span>
      </div>

      <textarea
        className="comment-area"
        placeholder="Share your thoughts, context, or examples..."
        value={v.comment}
        onChange={(e) => onChange({ ...v, comment: e.target.value })}
      />
    </div>
  );
}

function RatingCommentDisplay({ question, response }) {
  if (!response) return null;

  const { rating, comment } = response;

  return (
    <div className="response-display">
      <div className="response-question">
        <span>{question.label}</span>
        <div className="rating-blocks">
          {[1, 2, 3, 4, 5].map(n => (
            <div
              key={n}
              className={`rating-block ${n <= rating ? `filled-${rating}` : 'unfilled'}`}
            ></div>
          ))}
        </div>
      </div>
      <div className={`response-comment ${!comment ? 'empty' : ''}`}>
        {comment || 'No comment provided'}
      </div>
    </div>
  );
}

// MAIN APP
function App() {
  const [user, setUser] = useState(null);
  const [view, setView] = useState('login');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      apiCall('/api/auth/me')
        .then(userData => {
          setUser(userData);
          setView('home');
        })
        .catch(() => {
          localStorage.removeItem('token');
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const handleLogin = async (email, password) => {
    try {
      const data = await apiCall('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password })
      });
      localStorage.setItem('token', data.access_token);
      setUser(data.user);
      setView('home');
    } catch (err) {
      alert(err.message || 'Login failed');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setUser(null);
    setView('login');
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  if (view === 'login') {
    return <LoginScreen onLogin={handleLogin} />;
  }

  if (view === 'home') {
    return <HomeScreen user={user} onNavigate={setView} onLogout={handleLogout} />;
  }

  if (view === 'manager') {
    return <ManagerDashboard user={user} onLogout={handleLogout} onNavigate={setView} />;
  }

  if (view === 'team_member') {
    return <TeamMemberDashboard user={user} onLogout={handleLogout} onNavigate={setView} />;
  }

  return null;
}

// LOGIN SCREEN
function LoginScreen({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onLogin(email, password);
  };

  return (
    <div className="login-container">
      <div className="login-content fade-in">
        <div className="logo">P</div>
        <h1>PerformOS</h1>
        <h2>One-on-One Builder</h2>
        <p className="login-tagline">Better conversations. Safer teams. Stronger performance.</p>

        <div className="login-card">
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="alex@performos.io"
                required
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
              />
            </div>
            <button type="submit" className="btn-primary">Sign In</button>
          </form>
        </div>

        <div className="demo-accounts">
          <p><strong>Demo Accounts</strong></p>
          <p>Manager: alex@performos.io</p>
          <p>Team Members: sarah@performos.io, james@performos.io, priya@performos.io</p>
          <p>Password for all: demo</p>
        </div>
      </div>
    </div>
  );
}

// HOME SCREEN
function HomeScreen({ user, onNavigate, onLogout }) {
  return (
    <div className="home-container">
      <div className="home-content fade-in">
        <div className="logo">P</div>
        <h1>PerformOS</h1>
        <h2>One-on-One Builder</h2>

        <div className="role-cards">
          <div className="role-card fade-in-1" onClick={() => onNavigate('manager')}>
            <div className="role-icon">📊</div>
            <h3>Manager View</h3>
            <p>Run one-on-ones, review history, see team health and risk flags</p>
          </div>
          <div className="role-card fade-in-2" onClick={() => onNavigate('team_member')}>
            <div className="role-icon">💬</div>
            <h3>Team Member View</h3>
            <p>Complete pre-meeting reflections, view your own history</p>
          </div>
        </div>

        <div className="user-info">
          Signed in as {user.name} · <button onClick={onLogout} className="link-btn">Sign out</button>
        </div>
      </div>
    </div>
  );
}

// TEAM MEMBER DASHBOARD
function TeamMemberDashboard({ user, onLogout, onNavigate }) {
  const [weeks, setWeeks] = useState([]);
  const [scheduleStatus, setScheduleStatus] = useState([]);
  const [selectedWeek, setSelectedWeek] = useState(null);
  const [selectedSubmission, setSelectedSubmission] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [weeksData, statusData] = await Promise.all([
        apiCall('/api/schedule/weeks'),
        apiCall('/api/schedule/status')
      ]);
      setWeeks(weeksData.weeks);
      setScheduleStatus(statusData);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleWeekClick = async (date, isSubmitted) => {
    if (date > CURRENT_WEEK) return; // Future dates not clickable

    if (isSubmitted) {
      // Show submitted reflection
      const submission = await apiCall(`/api/submissions?date=${date}`);
      setSelectedSubmission(submission[0]);
      setSelectedWeek(null);
    } else if (date === CURRENT_WEEK) {
      // Open reflection form
      setSelectedWeek(date);
      setSelectedSubmission(null);
    }
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  if (selectedWeek) {
    return (
      <ReflectionForm
        date={selectedWeek}
        onBack={() => {
          setSelectedWeek(null);
          loadData();
        }}
        onSubmit={async (data) => {
          await apiCall('/api/submissions', {
            method: 'POST',
            body: JSON.stringify(data)
          });
          alert('Reflection submitted successfully!');
          setSelectedWeek(null);
          loadData();
        }}
      />
    );
  }

  if (selectedSubmission) {
    return (
      <SubmissionDisplay
        submission={selectedSubmission}
        onBack={() => setSelectedSubmission(null)}
      />
    );
  }

  return (
    <div className="dashboard-container">
      <nav className="navbar">
        <div className="nav-content">
          <div className="nav-left">
            <div className="logo-small">P</div>
            <span className="nav-title">PerformOS · My One-on-Ones</span>
          </div>
          <div className="nav-right">
            <span>{user.name}</span>
            <button onClick={() => onNavigate('home')} className="link-btn">← Home</button>
          </div>
        </div>
      </nav>

      <div className="dashboard-content">
        <div className="dashboard-header fade-in">
          <h1>My One-on-Ones</h1>
          <p>Your reflections, goals, and development in one place</p>
        </div>

        <div className="tab-content fade-in-1">
          <h3>Weekly Schedule</h3>
          <div className="weekly-schedule">
            {weeks.map((date, idx) => {
              const status = scheduleStatus.find(s => s.date === date);
              const isSubmitted = status?.submitted;
              const isCurrent = date === CURRENT_WEEK;
              const isPast = date < CURRENT_WEEK;
              const isFuture = date > CURRENT_WEEK;
              const isMissed = isPast && !isSubmitted;

              let statusDot = 'upcoming';
              let badgeText = 'Upcoming';
              let badgeClass = 'upcoming';

              if (isSubmitted) {
                statusDot = 'submitted';
                badgeText = 'Submitted';
                badgeClass = 'submitted';
              } else if (isCurrent) {
                statusDot = 'current';
                badgeText = 'Ready to complete';
                badgeClass = 'ready';
              } else if (isMissed) {
                statusDot = 'missed';
                badgeText = 'Missed';
                badgeClass = 'missed';
              }

              return (
                <div
                  key={date}
                  className={`week-row ${isFuture ? 'future' : ''}`}
                  onClick={() => !isFuture && handleWeekClick(date, isSubmitted)}
                  style={{ animationDelay: `${idx * 0.03}s` }}
                >
                  <div className={`status-dot ${statusDot}`}></div>
                  <div className="week-date">{formatDate(date)}</div>
                  {isCurrent && <div className="week-badge this-week">THIS WEEK</div>}
                  <div className={`week-badge ${badgeClass}`}>{badgeText}</div>
                  {!isFuture && <div className="arrow-icon">→</div>}
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}

// REFLECTION FORM
function ReflectionForm({ date, onBack, onSubmit }) {
  const [responses, setResponses] = useState({});

  const updateResponse = (questionId, value) => {
    setResponses(prev => ({ ...prev, [questionId]: value }));
  };

  const isValid = () => {
    const required = QUESTIONS.filter(q => !q.optional);
    return required.every(q => responses[q.id]?.rating > 0);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ date, responses });
  };

  const performanceQs = QUESTIONS.filter(q => q.section === 'performance');
  const wellbeingQs = QUESTIONS.filter(q => q.section === 'wellbeing');

  return (
    <div className="dashboard-container">
      <nav className="navbar">
        <div className="nav-content">
          <div className="nav-left">
            <div className="logo-small">P</div>
            <span className="nav-title">Weekly Reflection · {formatDateShort(date)}</span>
          </div>
        </div>
      </nav>

      <div className="dashboard-content">
        <button onClick={onBack} className="back-btn">← Back to schedule</button>

        <div className="reflection-form">
          <form onSubmit={handleSubmit}>
            <div className="form-section">
              <h2 className="section-title">Performance Reflection</h2>
              {performanceQs.map(q => (
                <RatingCommentInput
                  key={q.id}
                  question={q}
                  value={responses[q.id]}
                  onChange={(val) => updateResponse(q.id, val)}
                />
              ))}
            </div>

            <div className="form-section">
              <h2 className="section-title">Wellbeing & Safety</h2>
              {wellbeingQs.map(q => (
                <RatingCommentInput
                  key={q.id}
                  question={q}
                  value={responses[q.id]}
                  onChange={(val) => updateResponse(q.id, val)}
                />
              ))}
            </div>

            <div className="form-actions">
              <button type="button" onClick={onBack} className="btn-secondary">Cancel</button>
              <button type="submit" className="btn-primary" disabled={!isValid()}>
                Submit Reflection
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

// SUBMISSION DISPLAY
function SubmissionDisplay({ submission, onBack }) {
  const performanceQs = QUESTIONS.filter(q => q.section === 'performance');
  const wellbeingQs = QUESTIONS.filter(q => q.section === 'wellbeing');

  return (
    <div className="dashboard-container">
      <nav className="navbar">
        <div className="nav-content">
          <div className="nav-left">
            <div className="logo-small">P</div>
            <span className="nav-title">Reflection · {formatDateShort(submission.date)}</span>
          </div>
        </div>
      </nav>

      <div className="dashboard-content">
        <button onClick={onBack} className="back-btn">← Back to schedule</button>

        <div className="submission-display">
          <div className="tab-content">
            <h3>Performance Reflection</h3>
            {performanceQs.map(q => (
              <RatingCommentDisplay
                key={q.id}
                question={q}
                response={submission.responses[q.id]}
              />
            ))}
          </div>

          <div className="tab-content" style={{ marginTop: '20px' }}>
            <h3>Wellbeing & Safety</h3>
            {wellbeingQs.map(q => (
              <RatingCommentDisplay
                key={q.id}
                question={q}
                response={submission.responses[q.id]}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// MANAGER DASHBOARD
function ManagerDashboard({ user, onLogout, onNavigate }) {
  const [activeTab, setActiveTab] = useState('this-week');
  const [stats, setStats] = useState(null);
  const [thisWeekData, setThisWeekData] = useState([]);
  const [flags, setFlags] = useState([]);
  const [members, setMembers] = useState([]);
  const [selectedMemberSubmission, setSelectedMemberSubmission] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [statsData, thisWeekRes, flagsData, membersData] = await Promise.all([
        apiCall('/api/stats/dashboard'),
        apiCall('/api/this-week/submissions'),
        apiCall('/api/flags?status_filter=open'),
        apiCall('/api/members')
      ]);
      setStats(statsData);
      setThisWeekData(thisWeekRes);
      setFlags(flagsData);
      setMembers(membersData);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  if (selectedMemberSubmission) {
    return (
      <ManagerSubmissionDetail
        member={selectedMemberSubmission.member}
        submission={selectedMemberSubmission.submission}
        flags={flags.filter(f => f.member_id === selectedMemberSubmission.member._id)}
        onBack={() => setSelectedMemberSubmission(null)}
      />
    );
  }

  const healthColor = stats.team_health_score >= 80 ? '#10B981' : 
                       stats.team_health_score >= 60 ? '#06B6D4' : 
                       stats.team_health_score >= 40 ? '#F59E0B' : '#EF4444';

  return (
    <div className="dashboard-container">
      <nav className="navbar">
        <div className="nav-content">
          <div className="nav-left">
            <div className="logo-small">P</div>
            <span className="nav-title">PerformOS · Team One-on-Ones</span>
          </div>
          <div className="nav-right">
            <span>{user.name}</span>
            <button onClick={() => onNavigate('home')} className="link-btn">← Home</button>
          </div>
        </div>
      </nav>

      <div className="dashboard-content">
        <div className="dashboard-header fade-in">
          <h1>Team One-on-Ones</h1>
          <p>Performance conversations and team health at a glance</p>
        </div>

        <div className="metrics-grid fade-in-1">
          <div className="metric-card">
            <div className="metric-label">This Week</div>
            <div className="metric-value">{stats.this_week_submissions}/{stats.total_team_members}</div>
            <div className="metric-icon">📋</div>
          </div>
          <div className="metric-card">
            <div className="metric-label">Total Submissions</div>
            <div className="metric-value">{stats.total_submissions}</div>
            <div className="metric-icon">✓</div>
          </div>
          <div className="metric-card metric-hero" style={{ borderColor: healthColor }}>
            <div className="metric-label">Team Health</div>
            <div className="metric-value" style={{ color: healthColor }}>{stats.team_health_score}</div>
            <div className="metric-icon">♡</div>
            <div className="health-bar">
              <div className="health-bar-fill" style={{ width: `${stats.team_health_score}%`, background: healthColor }}></div>
            </div>
          </div>
          <div className="metric-card">
            <div className="metric-label">Active Flags</div>
            <div className="metric-value">{stats.active_flags}</div>
            <div className="metric-icon">⚑</div>
          </div>
        </div>

        <div className="tabs fade-in-2">
          <button 
            className={`tab ${activeTab === 'this-week' ? 'active' : ''}`}
            onClick={() => setActiveTab('this-week')}
          >
            This Week
            {thisWeekData.length > 0 && <span className="tab-badge">{thisWeekData.filter(d => d.has_submitted).length}/{thisWeekData.length}</span>}
          </button>
          <button 
            className={`tab ${activeTab === 'team-health' ? 'active' : ''}`}
            onClick={() => setActiveTab('team-health')}
          >
            Team Health
            {flags.length > 0 && <span className="tab-badge">{flags.length}</span>}
          </button>
        </div>

        {activeTab === 'this-week' && (
          <ThisWeekTab
            data={thisWeekData}
            flags={flags}
            onMemberClick={(member, submission) => setSelectedMemberSubmission({ member, submission })}
          />
        )}

        {activeTab === 'team-health' && (
          <TeamHealthTab
            flags={flags}
            members={members}
          />
        )}
      </div>
    </div>
  );
}

// THIS WEEK TAB
function ThisWeekTab({ data, flags, onMemberClick }) {
  if (data.length === 0) {
    return (
      <div className="tab-content">
        <div className="empty-state">
          <div className="empty-icon">📋</div>
          <h3>No team members</h3>
          <p>Team members will appear here once added</p>
        </div>
      </div>
    );
  }

  return (
    <div className="tab-content fade-in-3">
      <h3>Submissions This Week</h3>
      <div className="team-members-grid">
        {data.map(item => {
          const member = item.member;
          const submission = item.submission;
          const memberFlags = flags.filter(f => f.member_id === member._id);

          return (
            <div 
              key={member._id} 
              className="member-card"
              onClick={() => submission && onMemberClick(member, submission)}
              style={{ cursor: submission ? 'pointer' : 'default' }}
            >
              <div className="member-header">
                <Avatar name={member.name} size={52} />
                <div className="member-info">
                  <div className="member-name">{member.name}</div>
                  <div className="member-title">{member.title}</div>
                </div>
              </div>

              <div className="member-badges">
                {submission ? (
                  <>
                    <div className="badge submitted">Submitted</div>
                    {memberFlags.length > 0 && (
                      <div className="badge flag">{memberFlags.length} flag{memberFlags.length !== 1 ? 's' : ''}</div>
                    )}
                  </>
                ) : (
                  <div className="badge not-submitted">Not submitted</div>
                )}
              </div>

              {submission && (
                <div className="score-chips">
                  {['feeling_about_work', 'safe_to_raise_concerns', 'workload_manageable'].map(key => {
                    const response = submission.responses[key];
                    if (!response) return null;
                    const rating = response.rating;
                    const color = rating >= 4 ? 'green' : rating === 3 ? 'teal' : 'amber';
                    return <div key={key} className={`score-chip ${color}`}>{rating}</div>;
                  })}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

// TEAM HEALTH TAB
function TeamHealthTab({ flags, members }) {
  const getCategoryIcon = (cat) => {
    const icons = {
      wellbeing: '♡',
      psychological_safety: '🛡',
      workload: '⚡',
      engagement: '◎',
      team_dynamics: '👥',
      manager_gap: '⏰',
      performance_confidence: '📊'
    };
    return icons[cat] || '•';
  };

  const getCategoryLabel = (cat) => {
    const labels = {
      wellbeing: 'Wellbeing',
      psychological_safety: 'Psych Safety',
      workload: 'Workload',
      engagement: 'Engagement',
      team_dynamics: 'Team Dynamics',
      manager_gap: 'Manager Gap',
      performance_confidence: 'Performance'
    };
    return labels[cat] || cat;
  };

  const getMemberName = (memberId) => {
    const member = members.find(m => m._id === memberId);
    return member ? member.name : 'Unknown';
  };

  if (flags.length === 0) {
    return (
      <div className="tab-content">
        <div className="empty-state">
          <div className="empty-icon">✓</div>
          <h3>No active risk flags</h3>
          <p>Your team is in a healthy place</p>
        </div>
      </div>
    );
  }

  return (
    <div className="tab-content fade-in-3">
      <h3>Active Flags ({flags.length})</h3>
      <div className="flags-grid">
        {flags.map(flag => (
          <div key={flag._id} className={`flag-card ${flag.severity.replace('_', '-')}`}>
            <div className="flag-header">
              <div className="flag-member">{getMemberName(flag.member_id)}</div>
              <div className={`flag-severity ${flag.severity.replace('_', '-')}`}>
                {flag.severity.replace('_', ' ')}
              </div>
            </div>
            <div className="flag-category">
              <span>{getCategoryIcon(flag.category)}</span>
              <span>{getCategoryLabel(flag.category)}</span>
            </div>
            <div className="flag-signal">{flag.signal}</div>
            {flag.comment_snippet && (
              <div className="flag-comment-snippet">{flag.comment_snippet}</div>
            )}
            <div className="flag-date">Detected {formatDateShort(flag.date)}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

// MANAGER SUBMISSION DETAIL
function ManagerSubmissionDetail({ member, submission, flags, onBack }) {
  const performanceQs = QUESTIONS.filter(q => q.section === 'performance');
  const wellbeingQs = QUESTIONS.filter(q => q.section === 'wellbeing');

  return (
    <div className="dashboard-container">
      <nav className="navbar">
        <div className="nav-content">
          <div className="nav-left">
            <div className="logo-small">P</div>
            <span className="nav-title">{member.name}'s Reflection</span>
          </div>
        </div>
      </nav>

      <div className="dashboard-content">
        <button onClick={onBack} className="back-btn">← Back to dashboard</button>

        <div className="submission-display">
          <div className="submission-header">
            <Avatar name={member.name} size={56} />
            <div className="submission-info">
              <h2>{member.name}</h2>
              <div className="submission-meta">{member.title} · Week of {formatDateShort(submission.date)}</div>
            </div>
          </div>

          {flags.length > 0 && (
            <div className="tab-content" style={{ background: 'rgba(245, 158, 11, 0.05)', borderColor: '#F59E0B' }}>
              <h3>⚠️ Active Flags ({flags.length})</h3>
              <div style={{ fontSize: '14px', color: 'var(--gray-600)' }}>
                {flags.map((f, i) => (
                  <div key={i} style={{ marginBottom: '6px' }}>• {f.signal}</div>
                ))}
              </div>
            </div>
          )}

          <div className="tab-content" style={{ marginTop: '20px' }}>
            <h3>Performance Reflection</h3>
            {performanceQs.map(q => (
              <RatingCommentDisplay
                key={q.id}
                question={q}
                response={submission.responses[q.id]}
              />
            ))}
          </div>

          <div className="tab-content" style={{ marginTop: '20px' }}>
            <h3>Wellbeing & Safety</h3>
            {wellbeingQs.map(q => (
              <RatingCommentDisplay
                key={q.id}
                question={q}
                response={submission.responses[q.id]}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
