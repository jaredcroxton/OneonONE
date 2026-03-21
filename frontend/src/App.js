import React, { useState, useEffect, useMemo } from 'react';
import './App.css';

const API_BASE = process.env.REACT_APP_BACKEND_URL || '';
const CURRENT_WEEK = '2026-03-23';

// Utility functions
const getAvatarColor = (name) => {
  const colors = ['#3B82F6', '#14B8A6', '#22C55E', '#F59E0B', '#EC4899', '#8B5CF6'];
  return colors[name.length % colors.length];
};

const getScoreColor = (rating) => {
  if (rating >= 4) return '#22C55E';
  if (rating === 3) return '#14B8A6';
  return '#F59E0B';
};

const formatDate = (dateStr) => {
  if (!dateStr) return '—';
  const date = new Date(dateStr + 'T00:00:00');
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
};

const formatDateLong = (dateStr) => {
  if (!dateStr) return '—';
  const date = new Date(dateStr + 'T00:00:00');
  return date.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' });
};

const formatDateShort = (dateStr) => {
  if (!dateStr) return '—';
  const date = new Date(dateStr + 'T00:00:00');
  return date.toLocaleDateString('en-US', { day: 'numeric', month: 'short' });
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
    <div className="avatar" style={{ width: size, height: size, background: color }} data-testid="user-avatar">
      {initials}
      {healthStatus && <div className={`health-dot ${healthStatus}`} data-testid="health-status-dot"></div>}
    </div>
  );
}

function RatingCommentInput({ question, value, onChange, disabled }) {
  const v = value || { rating: 0, comment: '' };

  return (
    <div className="question-group" data-testid={`question-${question.id}`}>
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
              onClick={() => !disabled && onChange({ ...v, rating: n })}
              disabled={disabled}
              data-testid={`rating-${question.id}-${n}`}
            >
              {n}
            </button>
          ))}
        </div>
        <span className="rating-hint">{question.high}</span>
      </div>

      <div className="comment-box">
        <textarea
          className="reflection-textarea"
          placeholder="Add your thoughts..."
          value={v.comment}
          onChange={(e) => onChange({ ...v, comment: e.target.value })}
          rows={3}
          disabled={disabled}
          data-testid={`comment-${question.id}`}
        />
      </div>
    </div>
  );
}

function Sparkline({ data }) {
  if (!data || data.length === 0) return <span className="sparkline-empty">—</span>;
  
  const max = Math.max(...data, 1);
  const min = Math.min(...data, 0);
  const range = max - min || 1;
  
  return (
    <svg className="sparkline" width="80" height="24" viewBox="0 0 80 24">
      <polyline
        fill="none"
        stroke="var(--accent-teal)"
        strokeWidth="2"
        points={data.map((v, i) => `${(i / (data.length - 1 || 1)) * 80},${24 - ((v - min) / range) * 20}`).join(' ')}
      />
    </svg>
  );
}

function WeekCard({ week, onClick, isLocked, isCurrentWeek }) {
  const weekDate = new Date(week + 'T00:00:00');
  const dayNum = weekDate.getDate();
  const monthShort = weekDate.toLocaleDateString('en-US', { month: 'short' });
  
  return (
    <button
      className={`week-card ${isLocked ? 'locked' : 'unlocked'} ${isCurrentWeek ? 'current' : ''}`}
      onClick={onClick}
      disabled={isLocked}
      data-testid={`week-card-${week}`}
    >
      <div className="week-card-date">
        <div className="week-day">{dayNum}</div>
        <div className="week-month">{monthShort}</div>
      </div>
      {isLocked && (
        <div className="week-status locked" data-testid="week-status-locked">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
            <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
          </svg>
          Submitted
        </div>
      )}
      {!isLocked && isCurrentWeek && (
        <div className="week-status current" data-testid="week-status-current">This week</div>
      )}
      {!isLocked && !isCurrentWeek && (
        <div className="week-status unlocked" data-testid="week-status-unlocked">Open</div>
      )}
    </button>
  );
}

function Toast({ message, type, onClose }) {
  useEffect(() => {
    const timer = setTimeout(onClose, 4000);
    return () => clearTimeout(timer);
  }, [onClose]);

  return (
    <div className={`toast toast-${type}`} data-testid="toast-notification">
      <div className="toast-content">{message}</div>
      <button className="toast-close" onClick={onClose} data-testid="toast-close">×</button>
    </div>
  );
}

// MAIN APP
function App() {
  const [user, setUser] = useState(null);
  const [view, setView] = useState('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [toast, setToast] = useState(null);

  // Team Member State
  const [weeks, setWeeks] = useState([]);
  const [scheduleStatus, setScheduleStatus] = useState([]);
  const [selectedWeek, setSelectedWeek] = useState(null);
  const [formData, setFormData] = useState({});
  const [mySubmissions, setMySubmissions] = useState([]);

  // Manager State
  const [managerTab, setManagerTab] = useState('schedule');
  const [members, setMembers] = useState([]);
  const [dashboardStats, setDashboardStats] = useState(null);
  const [flags, setFlags] = useState([]);
  const [allSubmissions, setAllSubmissions] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    if (token && userData) {
      const parsedUser = JSON.parse(userData);
      setUser(parsedUser);
      setView(parsedUser.role === 'manager' ? 'manager' : 'team_member');
    }
  }, []);

  useEffect(() => {
    if (user && view === 'team_member') {
      loadTeamMemberData();
    } else if (user && view === 'manager') {
      loadManagerData();
    }
  }, [user, view]);

  const loadTeamMemberData = async () => {
    try {
      const [weeksData, statusData, submissionsData] = await Promise.all([
        apiCall('/api/schedule/weeks'),
        apiCall('/api/schedule/status'),
        apiCall('/api/submissions')
      ]);
      setWeeks(weeksData.weeks || []);
      setScheduleStatus(statusData || []);
      setMySubmissions(submissionsData || []);
    } catch (err) {
      console.error('Error loading team member data:', err);
      showToast('Failed to load data', 'error');
    }
  };

  const loadManagerData = async () => {
    try {
      const [membersData, statsData, flagsData, submissionsData] = await Promise.all([
        apiCall('/api/members'),
        apiCall('/api/stats/dashboard'),
        apiCall('/api/flags?status_filter=open'),
        apiCall('/api/submissions')
      ]);
      setMembers(membersData || []);
      setDashboardStats(statsData || {});
      setFlags(flagsData || []);
      setAllSubmissions(submissionsData || []);
    } catch (err) {
      console.error('Error loading manager data:', err);
      showToast('Failed to load dashboard', 'error');
    }
  };

  const showToast = (message, type = 'success') => {
    setToast({ message, type });
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const data = await apiCall('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password })
      });

      localStorage.setItem('token', data.access_token);
      localStorage.setItem('user', JSON.stringify(data.user));
      setUser(data.user);
      setView(data.user.role === 'manager' ? 'manager' : 'team_member');
      showToast(`Welcome back, ${data.user.name}!`);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    setView('login');
    setEmail('');
    setPassword('');
  };

  const handleWeekClick = (week) => {
    const status = scheduleStatus.find(s => s.date === week);
    if (status && status.submitted) {
      // View locked submission
      const submission = mySubmissions.find(s => s.date === week);
      if (submission) {
        setFormData(submission.responses || {});
        setSelectedWeek(week);
      }
    } else {
      // Open form for new submission
      setFormData({});
      setSelectedWeek(week);
    }
  };

  const handleSubmitReflection = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Validate all required questions
      const missingFields = QUESTIONS.filter(q => !q.optional).filter(q => {
        const val = formData[q.id];
        return !val || !val.rating || val.rating === 0;
      });

      if (missingFields.length > 0) {
        setError('Please complete all required questions with both a rating and comment.');
        setLoading(false);
        return;
      }

      await apiCall('/api/submissions', {
        method: 'POST',
        body: JSON.stringify({
          member_id: 'placeholder',
          date: selectedWeek,
          responses: formData
        })
      });

      showToast('Reflection submitted successfully!', 'success');
      setSelectedWeek(null);
      setFormData({});
      await loadTeamMemberData();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const calculateTrends = (submissions, field) => {
    return submissions
      .sort((a, b) => a.date.localeCompare(b.date))
      .map(sub => sub.responses?.[field]?.rating || 0)
      .filter(r => r > 0);
  };

  const getHealthStatus = (recentSubmissions) => {
    if (recentSubmissions.length === 0) return 'unknown';
    const latest = recentSubmissions[recentSubmissions.length - 1];
    const avgWellbeing = ['feeling_about_work', 'safe_to_raise_concerns', 'feel_supported', 'workload_manageable']
      .map(field => latest.responses?.[field]?.rating || 0)
      .filter(r => r > 0)
      .reduce((sum, r) => sum + r, 0) / 4;
    
    if (avgWellbeing >= 4) return 'good';
    if (avgWellbeing >= 3) return 'caution';
    return 'risk';
  };

  // LOGIN VIEW
  if (view === 'login') {
    return (
      <div className="app-shell">
        <div className="login-container">
          <div className="login-left">
            <div className="login-brand">
              <h1 className="brand-title" data-testid="app-title">PerformOS</h1>
              <p className="brand-subtitle">One-on-One Builder</p>
            </div>
            <p className="login-tagline">Structured conversations.<br/>Psychological safety insights.<br/>Better team outcomes.</p>
          </div>
          <div className="login-right">
            <form className="login-form" onSubmit={handleLogin} data-testid="login-form">
              <h2 className="login-title">Welcome back</h2>
              {error && <div className="error-message" data-testid="login-error">{error}</div>}
              <div className="form-group">
                <label htmlFor="email">Email</label>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  data-testid="login-email-input"
                />
              </div>
              <div className="form-group">
                <label htmlFor="password">Password</label>
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  data-testid="login-password-input"
                />
              </div>
              <button
                type="submit"
                className="btn-primary"
                disabled={loading}
                data-testid="login-submit-button"
              >
                {loading ? 'Signing in...' : 'Sign in'}
              </button>
              <div className="demo-credentials">
                <p className="demo-title">Demo Accounts</p>
                <p className="demo-item"><strong>Manager:</strong> alex@performos.io / demo</p>
                <p className="demo-item"><strong>Team Member:</strong> sarah@performos.io / demo</p>
              </div>
            </form>
          </div>
        </div>
        {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
      </div>
    );
  }

  // TEAM MEMBER VIEW
  if (view === 'team_member') {
    const isLocked = (week) => {
      const status = scheduleStatus.find(s => s.date === week);
      return status?.submitted || false;
    };

    const submissionForWeek = selectedWeek ? mySubmissions.find(s => s.date === selectedWeek) : null;
    const isViewingLocked = submissionForWeek && submissionForWeek.locked;

    return (
      <div className="app-shell">
        <header className="app-header">
          <div className="header-content">
            <h1 className="header-title" data-testid="app-title">PerformOS</h1>
            <div className="header-right">
              <Avatar name={user.name} size={36} />
              <div className="user-info">
                <div className="user-name" data-testid="user-name">{user.name}</div>
                <div className="user-role">{user.title || 'Team Member'}</div>
              </div>
              <button className="btn-secondary btn-sm" onClick={handleLogout} data-testid="logout-button">Sign out</button>
            </div>
          </div>
        </header>

        <main className="main-content">
          {!selectedWeek && (
            <>
              <section className="hero-section">
                <h2 className="section-title" data-testid="team-member-title">Your Weekly Check-ins</h2>
                <p className="section-subtitle">Share your progress, challenges, and how you're feeling with your manager.</p>
              </section>

              <section className="content-section light">
                <div className="content-container">
                  <div className="section-header">
                    <h3 className="section-heading">Weekly Schedule</h3>
                    <p className="section-description">Select a week to submit or review your reflection. Past submissions are locked and cannot be edited.</p>
                  </div>

                  <div className="weeks-grid" data-testid="weeks-grid">
                    {weeks.map(week => (
                      <WeekCard
                        key={week}
                        week={week}
                        onClick={() => handleWeekClick(week)}
                        isLocked={isLocked(week)}
                        isCurrentWeek={week === CURRENT_WEEK}
                      />
                    ))}
                  </div>
                </div>
              </section>

              <section className="content-section dark">
                <div className="content-container">
                  <div className="section-header">
                    <h3 className="section-heading">Your Trends</h3>
                    <p className="section-description">Track your wellbeing and confidence over time.</p>
                  </div>

                  <div className="trends-grid">
                    <div className="trend-card">
                      <div className="trend-label">Confidence in targets</div>
                      <Sparkline data={calculateTrends(mySubmissions, 'target_confidence')} />
                    </div>
                    <div className="trend-card">
                      <div className="trend-label">Feeling about work</div>
                      <Sparkline data={calculateTrends(mySubmissions, 'feeling_about_work')} />
                    </div>
                    <div className="trend-card">
                      <div className="trend-label">Psychological safety</div>
                      <Sparkline data={calculateTrends(mySubmissions, 'safe_to_raise_concerns')} />
                    </div>
                    <div className="trend-card">
                      <div className="trend-label">Team support</div>
                      <Sparkline data={calculateTrends(mySubmissions, 'feel_supported')} />
                    </div>
                    <div className="trend-card">
                      <div className="trend-label">Workload</div>
                      <Sparkline data={calculateTrends(mySubmissions, 'workload_manageable')} />
                    </div>
                  </div>

                  <div className="privacy-note">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <circle cx="12" cy="12" r="10"></circle>
                      <line x1="12" y1="16" x2="12" y2="12"></line>
                      <line x1="12" y1="8" x2="12.01" y2="8"></line>
                    </svg>
                    <span>Your reflections are private and only visible to you and your manager.</span>
                  </div>
                </div>
              </section>
            </>
          )}

          {selectedWeek && (
            <section className="content-section light">
              <div className="content-container">
                <div className="reflection-header">
                  <button className="btn-back" onClick={() => setSelectedWeek(null)} data-testid="back-button">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M19 12H5M12 19l-7-7 7-7"/>
                    </svg>
                    Back to schedule
                  </button>
                  <div className="reflection-title-row">
                    <h2 className="reflection-title" data-testid="reflection-title">
                      {isViewingLocked ? 'Your Reflection' : 'Weekly Reflection'}
                    </h2>
                    {isViewingLocked && (
                      <div className="locked-badge" data-testid="locked-badge">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                          <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                        </svg>
                        Submitted & Locked
                      </div>
                    )}
                  </div>
                  <p className="reflection-date">{formatDateLong(selectedWeek)}</p>
                  {isViewingLocked && (
                    <p className="reflection-note">This reflection has been submitted and locked. It cannot be edited.</p>
                  )}
                </div>

                <form className="reflection-form" onSubmit={handleSubmitReflection} data-testid="reflection-form">
                  {error && <div className="error-message" data-testid="reflection-error">{error}</div>}

                  <div className="questions-section">
                    <h3 className="section-subheading">Performance & Progress</h3>
                    {QUESTIONS.filter(q => q.section === 'performance').map(question => (
                      <RatingCommentInput
                        key={question.id}
                        question={question}
                        value={formData[question.id]}
                        onChange={(val) => setFormData({ ...formData, [question.id]: val })}
                        disabled={isViewingLocked}
                      />
                    ))}
                  </div>

                  <div className="questions-section">
                    <h3 className="section-subheading">Wellbeing & Support</h3>
                    {QUESTIONS.filter(q => q.section === 'wellbeing').map(question => (
                      <RatingCommentInput
                        key={question.id}
                        question={question}
                        value={formData[question.id]}
                        onChange={(val) => setFormData({ ...formData, [question.id]: val })}
                        disabled={isViewingLocked}
                      />
                    ))}
                  </div>

                  {!isViewingLocked && (
                    <div className="form-actions">
                      <button
                        type="button"
                        className="btn-secondary"
                        onClick={() => setSelectedWeek(null)}
                        data-testid="cancel-button"
                      >
                        Cancel
                      </button>
                      <button
                        type="submit"
                        className="btn-primary"
                        disabled={loading}
                        data-testid="submit-reflection-button"
                      >
                        {loading ? 'Submitting...' : 'Submit Reflection'}
                      </button>
                    </div>
                  )}
                </form>
              </div>
            </section>
          )}
        </main>

        {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
      </div>
    );
  }

  // MANAGER VIEW
  if (view === 'manager') {
    return (
      <div className="app-shell">
        <header className="app-header">
          <div className="header-content">
            <h1 className="header-title" data-testid="app-title">PerformOS</h1>
            <div className="header-right">
              <Avatar name={user.name} size={36} />
              <div className="user-info">
                <div className="user-name" data-testid="user-name">{user.name}</div>
                <div className="user-role">{user.title || 'Manager'}</div>
              </div>
              <button className="btn-secondary btn-sm" onClick={handleLogout} data-testid="logout-button">Sign out</button>
            </div>
          </div>
        </header>

        <main className="main-content">
          <section className="hero-section">
            <h2 className="section-title" data-testid="manager-title">Team Dashboard</h2>
            <p className="section-subtitle">Monitor team health, track one-on-ones, and address psychological safety signals.</p>
          </section>

          <section className="content-section dark">
            <div className="content-container">
              <div className="kpi-grid">
                <div className="kpi-card">
                  <div className="kpi-label">This Week's Submissions</div>
                  <div className="kpi-value" data-testid="kpi-submissions">{dashboardStats?.this_week_submissions || 0} / {dashboardStats?.total_team_members || 0}</div>
                </div>
                <div className="kpi-card">
                  <div className="kpi-label">Total Completed</div>
                  <div className="kpi-value" data-testid="kpi-completed">{dashboardStats?.total_submissions || 0}</div>
                </div>
                <div className="kpi-card">
                  <div className="kpi-label">Team Health Score</div>
                  <div className="kpi-value" data-testid="kpi-health-score">{dashboardStats?.team_health_score || 0}%</div>
                </div>
                <div className="kpi-card">
                  <div className="kpi-label">Active Flags</div>
                  <div className="kpi-value" style={{ color: flags.length > 0 ? '#F59E0B' : '#22C55E' }} data-testid="kpi-flags">{flags.length}</div>
                </div>
              </div>
            </div>
          </section>

          <section className="content-section light">
            <div className="content-container">
              <div className="tabs" data-testid="manager-tabs">
                <button
                  className={`tab ${managerTab === 'schedule' ? 'active' : ''}`}
                  onClick={() => setManagerTab('schedule')}
                  data-testid="tab-schedule"
                >
                  Schedule
                </button>
                <button
                  className={`tab ${managerTab === 'team_health' ? 'active' : ''}`}
                  onClick={() => setManagerTab('team_health')}
                  data-testid="tab-team-health"
                >
                  Team Health
                  {flags.length > 0 && <span className="tab-badge">{flags.length}</span>}
                </button>
                <button
                  className={`tab ${managerTab === 'performance' ? 'active' : ''}`}
                  onClick={() => setManagerTab('performance')}
                  data-testid="tab-performance"
                >
                  Performance Trends
                </button>
              </div>

              {managerTab === 'schedule' && (
                <div className="tab-content" data-testid="schedule-content">
                  <div className="table-container">
                    <table className="data-table">
                      <thead>
                        <tr>
                          <th>Team Member</th>
                          <th>Title</th>
                          <th>This Week</th>
                          <th>Recent Trends</th>
                        </tr>
                      </thead>
                      <tbody>
                        {members.map(member => {
                          const memberSubmissions = allSubmissions.filter(s => s.member_id === member._id);
                          const healthStatus = getHealthStatus(memberSubmissions);
                          return (
                            <tr key={member._id} data-testid={`member-row-${member._id}`}>
                              <td>
                                <div className="member-cell">
                                  <Avatar name={member.name} size={40} healthStatus={healthStatus} />
                                  <span className="member-name">{member.name}</span>
                                </div>
                              </td>
                              <td>{member.title}</td>
                              <td>
                                {memberSubmissions.find(s => s.date === CURRENT_WEEK) ? (
                                  <span className="status-badge submitted" data-testid="status-submitted">Submitted</span>
                                ) : (
                                  <span className="status-badge pending" data-testid="status-pending">Pending</span>
                                )}
                              </td>
                              <td>
                                <Sparkline data={calculateTrends(memberSubmissions, 'feeling_about_work')} />
                              </td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {managerTab === 'team_health' && (
                <div className="tab-content" data-testid="team-health-content">
                  <div className="section-header">
                    <h3 className="section-heading">Active Signals</h3>
                    <p className="section-description">Psychological safety and wellbeing signals detected across your team.</p>
                  </div>

                  {flags.length === 0 ? (
                    <div className="empty-state">
                      <p>No active signals detected. Your team appears to be doing well.</p>
                    </div>
                  ) : (
                    <div className="flags-list">
                      {flags.map(flag => {
                        const member = members.find(m => m._id === flag.member_id);
                        return (
                          <div key={flag._id} className="flag-card" data-testid={`flag-${flag._id}`}>
                            <div className="flag-header">
                              <div className="flag-member">
                                {member && <Avatar name={member.name} size={32} />}
                                <div className="flag-member-info">
                                  <div className="flag-member-name">{member?.name || 'Unknown'}</div>
                                  <div className="flag-date">{formatDate(flag.date)}</div>
                                </div>
                              </div>
                              <span className={`severity-badge ${flag.severity}`} data-testid="flag-severity">
                                {flag.severity === 'action_required' ? 'Action Required' : flag.severity === 'concern' ? 'Concern' : 'Watch'}
                              </span>
                            </div>
                            <div className="flag-body">
                              <div className="flag-category">{flag.category.replace('_', ' ')}</div>
                              <div className="flag-signal">{flag.signal}</div>
                              {flag.comment_snippet && (
                                <div className="flag-quote" data-testid="flag-quote">
                                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M6 17h3l2-4V7H5v6h3zm8 0h3l2-4V7h-6v6h3z"/>
                                  </svg>
                                  "{flag.comment_snippet}"
                                </div>
                              )}
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  )}
                </div>
              )}

              {managerTab === 'performance' && (
                <div className="tab-content" data-testid="performance-content">
                  <div className="section-header">
                    <h3 className="section-heading">Team Performance Trends</h3>
                    <p className="section-description">Monitor confidence and progress across your team.</p>
                  </div>

                  <div className="performance-grid">
                    {members.map(member => {
                      const memberSubmissions = allSubmissions.filter(s => s.member_id === member._id);
                      return (
                        <div key={member._id} className="performance-card" data-testid={`performance-${member._id}`}>
                          <div className="performance-header">
                            <Avatar name={member.name} size={36} />
                            <div className="performance-member-info">
                              <div className="performance-member-name">{member.name}</div>
                              <div className="performance-member-title">{member.title}</div>
                            </div>
                          </div>
                          <div className="performance-metrics">
                            <div className="metric-row">
                              <span className="metric-label">Target Confidence</span>
                              <Sparkline data={calculateTrends(memberSubmissions, 'target_confidence')} />
                            </div>
                            <div className="metric-row">
                              <span className="metric-label">Wellbeing</span>
                              <Sparkline data={calculateTrends(memberSubmissions, 'feeling_about_work')} />
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}
            </div>
          </section>
        </main>

        {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
      </div>
    );
  }

  return null;
}

export default App;
