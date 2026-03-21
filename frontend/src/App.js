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
  if (rating >= 4) return '#10B981';  // Green for 4-5
  if (rating >= 2) return '#F59E0B';  // Amber for 2-3
  return '#EF4444';                    // Red for 1
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

function TrendCard({ metricKey, submissions, dark, compact }) {
  const wellbeingLabels = {
    feeling_about_work: "Feeling about work",
    safe_to_raise_concerns: "Psychological safety",
    feel_supported: "Team support",
    workload_manageable: "Workload",
    target_confidence: "Confidence in targets"
  };
  
  const wellbeingSubs = {
    feeling_about_work: "How are you feeling about work?",
    safe_to_raise_concerns: "Do you feel safe raising concerns?",
    feel_supported: "How supported do you feel?",
    workload_manageable: "Is your workload manageable?",
    target_confidence: "Confidence in hitting targets"
  };
  
  const label = wellbeingLabels[metricKey] || metricKey;
  const subtitle = wellbeingSubs[metricKey] || "";
  const data = submissions
    .map(s => ({ rating: s.responses?.[metricKey]?.rating, date: s.date }))
    .filter(d => d.rating != null)
    .sort((a, b) => a.date.localeCompare(b.date));
  
  if (data.length === 0) return null;

  // Calculate AVERAGE rating instead of latest
  const avg = data.reduce((sum, d) => sum + d.rating, 0) / data.length;
  const latest = data[data.length - 1].rating;
  const first = data[0].rating;
  const delta = data.length >= 2 ? latest - first : 0;
  const col = getScoreColor(avg);

  const deltaText = delta > 0 
    ? `▲ ${Math.abs(delta).toFixed(1)} improving` 
    : delta < 0 
    ? `▼ ${Math.abs(delta).toFixed(1)} declining` 
    : data.length >= 2 ? "— Stable" : "";
  const deltaCol = delta > 0 ? "#10B981" : delta < 0 ? "#EF4444" : "var(--text-on-dark-muted)";

  const barHeight = compact ? 32 : 48;

  return (
    <div className={`trend-card-v4 ${dark ? 'dark' : 'light'} ${compact ? 'compact' : ''}`} data-testid={`trend-${metricKey}`}>
      <div className="trend-header">
        <div className="trend-label-row">
          <div className="trend-label">{label}</div>
          <div className="trend-score-col">
            <div className="trend-score" style={{ color: col }}>{avg.toFixed(1)}/5</div>
            <div className="trend-score-label">avg</div>
          </div>
        </div>
        {!compact && subtitle && <div className="trend-subtitle">{subtitle}</div>}
        {deltaText && (
          <div className="trend-delta" style={{ color: deltaCol }}>
            {deltaText}
          </div>
        )}
      </div>

      <div className="trend-bars" style={{ height: barHeight }}>
        {data.map((d, i) => {
          const pct = (d.rating / 5) * 100;
          const barColor = getScoreColor(d.rating);
          const isLatest = i === data.length - 1;
          return (
            <div 
              key={i}
              className="trend-bar"
              style={{
                height: `${pct}%`,
                background: barColor,
                opacity: isLatest ? 1 : 0.7
              }}
              data-testid={`trend-bar-${i}`}
            />
          );
        })}
      </div>

      {!compact && (
        <div className="trend-dates">
          {data.map((d, i) => (
            <div key={i} className="trend-date">{formatDateShort(d.date)}</div>
          ))}
        </div>
      )}
    </div>
  );
}

function MiniTrendBars({ data }) {
  if (!data || data.length < 2) return <span className="sparkline-empty">—</span>;
  
  const latest = data[data.length - 1];
  const col = getScoreColor(latest);
  
  return (
    <div className="mini-trend-bars">
      {data.map((v, i) => {
        const pct = (v / 5) * 100;
        const barColor = getScoreColor(v);
        return (
          <div
            key={i}
            className="mini-bar"
            style={{
              height: `${pct}%`,
              background: barColor,
              opacity: i === data.length - 1 ? 1 : 0.7
            }}
          />
        );
      })}
    </div>
  );
}

function ScoreChips({ submission }) {
  const metrics = ['feeling_about_work', 'safe_to_raise_concerns', 'workload_manageable'];
  return (
    <div className="score-chips">
      {metrics.map(metric => {
        const rating = submission.responses?.[metric]?.rating;
        if (!rating) return <div key={metric} className="score-chip empty">—</div>;
        const color = getScoreColor(rating);
        return (
          <div 
            key={metric} 
            className="score-chip"
            style={{ background: color }}
            title={metric.replace(/_/g, ' ')}
          >
            {rating}
          </div>
        );
      })}
    </div>
  );
}

function RatingCommentDisplay({ question, value }) {
  const v = value || { rating: 0, comment: '' };
  const color = getScoreColor(v.rating);
  
  return (
    <div className="question-group-display">
      <div className="question-label">{question.label}</div>
      
      <div className="rating-display">
        <span className="rating-display-label">{question.ratingLabel}</span>
        <div className="rating-blocks">
          {[1, 2, 3, 4, 5].map(n => (
            <div
              key={n}
              className={`rating-block ${v.rating === n ? 'selected' : ''}`}
              style={v.rating === n ? { background: color, borderColor: color } : {}}
            >
              {n}
            </div>
          ))}
        </div>
      </div>

      {v.comment && (
        <div className="comment-display">
          <div className="comment-display-label">Comment:</div>
          <div className="comment-display-text">{v.comment}</div>
        </div>
      )}
    </div>
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
  const [historyMember, setHistoryMember] = useState(null);
  const [viewedSubmission, setViewedSubmission] = useState(null);
  const [healthDetailMember, setHealthDetailMember] = useState(null);
  const [briefing, setBriefing] = useState(null);
  const [briefingLoading, setBriefingLoading] = useState(false);
  const [coaching, setCoaching] = useState(null);
  const [coachingLoading, setCoachingLoading] = useState(false);
  
  // Executive State
  const [selectedTeam, setSelectedTeam] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    if (token && userData) {
      const parsedUser = JSON.parse(userData);
      setUser(parsedUser);
      
      if (parsedUser.role === 'manager') {
        setView('manager');
      } else if (parsedUser.role === 'executive') {
        setView('executive');
      } else {
        setView('team_member');
      }
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
      
      // Set view based on role
      if (data.user.role === 'manager') {
        setView('manager');
      } else if (data.user.role === 'executive') {
        setView('executive');
      } else {
        setView('team_member');
      }
      
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

  // Simulated org-wide team data for executive view
  const orgTeams = useMemo(() => {
    // Engineering - calculated from real data
    const engHealth = dashboardStats?.team_health_score || 0;
    const engFlags = flags.filter(f => f.status === 'open').length;
    const engAtRisk = members.filter(m => {
      const memberSubs = allSubmissions.filter(s => s.member_id === m._id);
      const health = getHealthStatus(memberSubs);
      return health === 'risk';
    }).length;

    return [
      {
        id: 'team_cs',
        name: 'Customer Success',
        manager: 'Liam Park',
        headcount: 7,
        health: 41,
        trend: [65, 60, 55, 48, 41],
        activeFlags: 5,
        riskMembers: 2,
        attrition: [
          { role: 'CS Team Lead', risk: 71, reason: 'Wellbeing dropped 4→2, workload at 1/5, raised issues 4 times with no resolution' },
          { role: 'Account Manager', risk: 55, reason: 'Missed 2 reflections, responses declining, minimal comments' }
        ]
      },
      {
        id: 'team_design',
        name: 'Design',
        manager: 'Mia Chen',
        headcount: 4,
        health: 58,
        trend: [72, 68, 64, 60, 58],
        activeFlags: 3,
        riskMembers: 1,
        attrition: [
          { role: 'Senior Designer', risk: 62, reason: 'Support score declining, workload increasing, 2 flags unresolved for 3+ weeks' }
        ]
      },
      {
        id: 'team_eng',
        name: 'Engineering',
        manager: 'Alex Chen',
        headcount: 6,
        health: engHealth,
        trend: [68, 65, 62, 58, engHealth],
        activeFlags: engFlags,
        riskMembers: engAtRisk,
        attrition: engAtRisk > 0 ? [
          { role: 'Backend Engineer', risk: 78, reason: 'Workload at 1/5 for two weeks, wellbeing at 2/5, burnout signals' }
        ] : []
      },
      {
        id: 'team_sales',
        name: 'Sales',
        manager: 'Jordan Blake',
        headcount: 8,
        health: 79,
        trend: [76, 78, 75, 77, 79],
        activeFlags: 1,
        riskMembers: 0,
        attrition: []
      },
      {
        id: 'team_data',
        name: 'Data & Analytics',
        manager: 'Kai Patel',
        headcount: 4,
        health: 82,
        trend: [78, 80, 79, 81, 82],
        activeFlags: 0,
        riskMembers: 0,
        attrition: []
      },
      {
        id: 'team_product',
        name: 'Product',
        manager: 'Sam Nakamura',
        headcount: 5,
        health: 88,
        trend: [82, 84, 85, 86, 88],
        activeFlags: 0,
        riskMembers: 0,
        attrition: []
      }
    ].sort((a, b) => a.health - b.health); // Sort worst-first
  }, [dashboardStats, flags, members, allSubmissions]);

  const generateBriefing = async () => {
    setBriefingLoading(true);
    try {
      // Build team data summary
      const teamData = members.map(member => {
        const memberSubs = allSubmissions.filter(s => s.member_id === member._id).sort((a, b) => a.date.localeCompare(b.date));
        const memberFlags = flags.filter(f => f.member_id === member._id && f.status === 'open');
        
        if (memberSubs.length === 0) return null;
        
        const latest = memberSubs[memberSubs.length - 1];
        const wellbeingMetrics = ['feeling_about_work', 'safe_to_raise_concerns', 'feel_supported', 'workload_manageable', 'target_confidence'];
        
        const scores = {};
        const trends = {};
        wellbeingMetrics.forEach(metric => {
          const values = memberSubs.map(s => s.responses?.[metric]?.rating).filter(Boolean);
          if (values.length > 0) {
            scores[metric] = (values.reduce((a, b) => a + b, 0) / values.length).toFixed(1);
            if (values.length >= 2) {
              const delta = values[values.length - 1] - values[0];
              trends[metric] = delta > 0 ? 'improving' : delta < 0 ? 'declining' : 'stable';
            }
          }
        });
        
        const healthScore = (Object.values(scores).reduce((a, b) => a + parseFloat(b), 0) / Object.keys(scores).length / 5) * 100;
        
        return {
          name: member.name,
          title: member.title,
          healthScore: Math.round(healthScore),
          scores,
          trends,
          flags: memberFlags.map(f => ({ severity: f.severity, signal: f.signal, category: f.category })),
          latestComment: latest.responses?.feeling_about_work?.comment || latest.responses?.workload_manageable?.comment || ''
        };
      }).filter(Boolean);

      const teamHealthScore = dashboardStats?.team_health_score || 0;
      const activeFlags = flags.filter(f => f.status === 'open').length;

      // Build prompt
      const prompt = `You are an expert leadership coach and team health advisor. Based on the team data below, generate a structured daily briefing for the manager to use this week.

TEAM DATA:
${teamData.map(m => `
- ${m.name}, ${m.title}
- Health score: ${m.healthScore}/100
- Scores (avg): feeling=${m.scores.feeling_about_work || 'N/A'}, safety=${m.scores.safe_to_raise_concerns || 'N/A'}, support=${m.scores.feel_supported || 'N/A'}, workload=${m.scores.workload_manageable || 'N/A'}, confidence=${m.scores.target_confidence || 'N/A'}
- Trends: ${Object.entries(m.trends).map(([k, v]) => `${k}:${v}`).join(', ')}
- Active flags: ${m.flags.length > 0 ? m.flags.map(f => `${f.severity} - ${f.signal}`).join('; ') : 'None'}
- Latest comment: "${m.latestComment}"
`).join('\n')}

TEAM HEALTH SCORE: ${teamHealthScore}/100
ACTIVE FLAGS: ${activeFlags}

Generate a JSON response with NO markdown, NO backticks, just raw JSON:
{
  "team_pulse": "2-3 sentence summary of overall team state — be specific, reference people and scores",
  "priority_actions": [
    {"person": "Name", "action": "Specific action", "urgency": "today|this_week|next_1on1", "reason": "Why"}
  ],
  "daily_briefing": {
    "opening": "Suggested 2-sentence opening for daily standup that acknowledges wins and sets supportive tone",
    "watch_items": ["Specific thing to observe today"],
    "conversation_starters": [
      {"person": "Name", "starter": "Natural, human way to check in — not clinical"}
    ]
  },
  "wellbeing_activities": [
    {"activity": "Specific team activity", "target": "What risk it addresses", "duration": "Time estimate"}
  ],
  "recognition": [
    {"person": "Name", "what": "Specific achievement to recognise"}
  ],
  "risks_to_watch": [
    {"person": "Name", "risk": "What could go wrong without action", "timeframe": "How urgent"}
  ]
}

RULES:
- Be specific. Reference actual scores and comments.
- Priority actions ordered by urgency (today first). Max 4.
- Conversation starters must feel human. NOT "I noticed your score dropped". More like "How did the on-call go? I've been thinking about it."
- Wellbeing activities should be practical, not corporate fluff. Max 3.
- Recognition highlights genuine contributions. Max 3.
- If someone is doing well, say so.`;

      // Call OpenAI API (using provided key)
      const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer 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'
        },
        body: JSON.stringify({
          model: 'gpt-4-turbo-preview',
          messages: [{ role: 'user', content: prompt }],
          max_tokens: 2000,
          temperature: 0.7
        })
      });

      if (!response.ok) {
        throw new Error('Failed to generate briefing');
      }

      const data = await response.json();
      const briefingText = data.choices[0].message.content;
      
      // Parse JSON response
      const briefingData = JSON.parse(briefingText.replace(/```json\n?|\n?```/g, '').trim());
      setBriefing(briefingData);
    } catch (err) {
      console.error('Error generating briefing:', err);
      showToast('Failed to generate briefing. Please try again.', 'error');
    } finally {
      setBriefingLoading(false);
    }
  };

  const generateCoaching = async () => {
    setCoachingLoading(true);
    try {
      // Calculate days each flag has been open
      const today = new Date(CURRENT_WEEK);
      const activeFlagsWithDays = flags.filter(f => f.status === 'open').map(flag => {
        const flagDate = new Date(flag.date);
        const daysOpen = Math.floor((today - flagDate) / (1000 * 60 * 60 * 24));
        const member = members.find(m => m._id === flag.member_id);
        return {
          member: member?.name || 'Unknown',
          category: flag.category,
          severity: flag.severity,
          signal: flag.signal,
          dateCreated: flag.date,
          daysOpen,
          status: flag.status
        };
      });

      // Calculate team trends
      const teamTrends = members.map(member => {
        const memberSubs = allSubmissions.filter(s => s.member_id === member._id).sort((a, b) => a.date.localeCompare(b.date));
        if (memberSubs.length < 2) return null;

        const wellbeingMetrics = ['feeling_about_work', 'safe_to_raise_concerns', 'workload_manageable'];
        const trends = {};
        wellbeingMetrics.forEach(metric => {
          const values = memberSubs.map(s => s.responses?.[metric]?.rating).filter(Boolean);
          if (values.length >= 2) {
            const delta = values[values.length - 1] - values[0];
            trends[metric] = delta < 0 ? 'declining' : delta > 0 ? 'improving' : 'stable';
          }
        });

        const hasDecline = Object.values(trends).some(t => t === 'declining');
        return {
          name: member.name,
          wellbeingTrend: hasDecline ? 'declining' : 'stable',
          declining: Object.entries(trends).filter(([k, v]) => v === 'declining').map(([k]) => k)
        };
      }).filter(Boolean);

      const teamHealthScore = dashboardStats?.team_health_score || 0;

      // Build coaching prompt for Claude
      const prompt = `You are a private executive coach for a people manager. Your job is to give them honest, actionable coaching on how they're managing their team's wellbeing and performance — based on real data, not generic advice.

MANAGER: ${user.name}, ${user.title || 'Manager'}
TEAM SIZE: ${members.length}
TEAM HEALTH: ${teamHealthScore}/100

ACTIVE FLAGS:
${activeFlagsWithDays.map(f => `- ${f.member}: ${f.category} (${f.severity}) - "${f.signal}" - Created ${f.dateCreated}, ${f.daysOpen} days open, status: ${f.status}`).join('\n')}

TEAM TRENDS:
${teamTrends.map(t => `- ${t.name}: wellbeing ${t.wellbeingTrend}${t.declining.length > 0 ? ', declining metrics: ' + t.declining.join(', ') : ''}`).join('\n')}

Generate a JSON response with NO markdown, NO backticks:
{
  "coaching_summary": "2-3 sentences on how the manager is doing overall — be honest but constructive. Reference specific flags and timelines.",
  "strengths": [
    "Something specific the manager is doing well based on the data"
  ],
  "gaps": [
    {"issue": "Specific gap in their management response", "impact": "What this is causing for the team member", "suggestion": "Concrete action with a framework or script they can use"}
  ],
  "overdue_actions": [
    {"flag": "Which flag", "days_open": 14, "person": "Name", "script": "A word-for-word conversation opener the manager can use this week — warm, human, not HR-scripted"}
  ],
  "skill_building": [
    {"skill": "A specific management skill to develop", "why": "Why this matters based on current team data", "practice": "One thing to try this week to build this skill"}
  ],
  "weekly_challenge": "One specific thing to do differently this week — make it concrete and measurable"
}

RULES:
- Be direct. If the manager has left a flag unresolved for 3 weeks, say so clearly.
- Frame gaps as growth opportunities, not failures.
- Conversation scripts must sound like a real human talking, not a HR template. Example: "Priya, I've been reflecting on the team meeting two weeks ago and I think I missed something. Can you tell me how you experienced that? I want to make sure your perspective is heard."
- Skill building should connect to the actual gaps — if the issue is unresolved psych safety flags, the skill might be "having difficult conversations about team dynamics."
- The weekly challenge should be specific enough that the manager can tell if they did it or not.
- Maximum 3 strengths, 3 gaps, 3 overdue actions, 2 skill building items.`;

      // Call Anthropic Claude API via backend
      const response = await fetch(`${API_BASE}/api/generate-coaching`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ prompt })
      });

      if (!response.ok) {
        throw new Error('Failed to generate coaching');
      }

      const data = await response.json();
      const coachingText = data.content[0].text;
      
      // Parse JSON response
      const coachingData = JSON.parse(coachingText.replace(/```json\n?|\n?```/g, '').trim());
      setCoaching(coachingData);
    } catch (err) {
      console.error('Error generating coaching:', err);
      showToast('Failed to generate coaching. Please try again.', 'error');
    } finally {
      setCoachingLoading(false);
    }
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
                <p className="demo-item"><strong>Executive:</strong> rachel@performos.io / demo</p>
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

                  <div className="trends-layout">
                    <div className="trends-primary">
                      <TrendCard metricKey="feeling_about_work" submissions={mySubmissions} dark={true} />
                      <TrendCard metricKey="safe_to_raise_concerns" submissions={mySubmissions} dark={true} />
                      <TrendCard metricKey="feel_supported" submissions={mySubmissions} dark={true} />
                    </div>
                    <div className="trends-secondary">
                      <TrendCard metricKey="workload_manageable" submissions={mySubmissions} dark={true} compact={true} />
                      <TrendCard metricKey="target_confidence" submissions={mySubmissions} dark={true} compact={true} />
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
                <button
                  className={`tab ${managerTab === 'ai_briefing' ? 'active' : ''}`}
                  onClick={() => setManagerTab('ai_briefing')}
                  data-testid="tab-ai-briefing"
                >
                  AI Briefing
                </button>
                <button
                  className={`tab ${managerTab === 'coaching' ? 'active' : ''}`}
                  onClick={() => setManagerTab('coaching')}
                  data-testid="tab-coaching"
                >
                  My Coaching
                </button>
              </div>

              {managerTab === 'schedule' && !historyMember && !viewedSubmission && (
                <div className="tab-content" data-testid="schedule-content">
                  <div className="table-container">
                    <table className="data-table">
                      <thead>
                        <tr>
                          <th style={{ width: '30%' }}>Team Member</th>
                          <th style={{ width: '25%' }}>Title</th>
                          <th style={{ width: '20%' }}>This Week</th>
                          <th style={{ width: '25%' }}>History</th>
                        </tr>
                      </thead>
                      <tbody>
                        {members.map(member => {
                          const memberSubmissions = allSubmissions.filter(s => s.member_id === member._id);
                          const healthStatus = getHealthStatus(memberSubmissions);
                          const thisWeekSubmission = memberSubmissions.find(s => s.date === CURRENT_WEEK);
                          const hasSubmitted = !!thisWeekSubmission;
                          
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
                                {hasSubmitted ? (
                                  <span 
                                    className="status-badge submitted clickable" 
                                    data-testid="status-submitted"
                                    onClick={() => setViewedSubmission(thisWeekSubmission)}
                                  >
                                    Submitted
                                  </span>
                                ) : (
                                  <span className="status-badge pending" data-testid="status-pending">Not submitted</span>
                                )}
                              </td>
                              <td>
                                <button
                                  className="view-history-link"
                                  onClick={() => setHistoryMember(member)}
                                  data-testid={`view-history-${member._id}`}
                                >
                                  View history →
                                </button>
                              </td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {managerTab === 'schedule' && historyMember && !viewedSubmission && (
                <div className="tab-content" data-testid="history-panel">
                  <div className="history-panel">
                    <div className="history-header">
                      <button className="btn-back" onClick={() => setHistoryMember(null)} data-testid="back-to-schedule">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <path d="M19 12H5M12 19l-7-7 7-7"/>
                        </svg>
                        Back
                      </button>
                      <div className="history-member-info">
                        <Avatar name={historyMember.name} size={48} />
                        <div>
                          <div className="history-member-name">{historyMember.name}</div>
                          <div className="history-member-title">{historyMember.title}</div>
                        </div>
                      </div>
                    </div>

                    <div className="history-submissions">
                      <h3 className="history-title">Submission history ({allSubmissions.filter(s => s.member_id === historyMember._id).length} weeks)</h3>
                      
                      <div className="history-list">
                        {allSubmissions
                          .filter(s => s.member_id === historyMember._id)
                          .sort((a, b) => b.date.localeCompare(a.date))
                          .map(submission => (
                            <button
                              key={submission._id}
                              className="history-row"
                              onClick={() => setViewedSubmission(submission)}
                              data-testid={`history-row-${submission.date}`}
                            >
                              <div className="history-date">{formatDateLong(submission.date)}</div>
                              <div className="history-row-right">
                                <ScoreChips submission={submission} />
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                  <path d="M5 12h14M12 5l7 7-7 7"/>
                                </svg>
                              </div>
                            </button>
                          ))}
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {managerTab === 'schedule' && viewedSubmission && (
                <div className="tab-content" data-testid="submission-detail">
                  <div className="submission-detail">
                    <button 
                      className="btn-back" 
                      onClick={() => setViewedSubmission(null)} 
                      data-testid="back-from-detail"
                    >
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M19 12H5M12 19l-7-7 7-7"/>
                      </svg>
                      {historyMember ? 'Back to history' : 'Back to schedule'}
                    </button>

                    <div className="submission-detail-header">
                      <Avatar name={members.find(m => m._id === viewedSubmission.member_id)?.name || 'Unknown'} size={56} />
                      <div>
                        <h2 className="submission-detail-name">{members.find(m => m._id === viewedSubmission.member_id)?.name || 'Unknown'}</h2>
                        <div className="submission-detail-date">{formatDateLong(viewedSubmission.date)}</div>
                      </div>
                    </div>

                    <div className="submission-detail-content">
                      <div className="questions-section">
                        <h3 className="section-subheading">Performance & Progress</h3>
                        {QUESTIONS.filter(q => q.section === 'performance').map(question => (
                          <RatingCommentDisplay
                            key={question.id}
                            question={question}
                            value={viewedSubmission.responses?.[question.id]}
                          />
                        ))}
                      </div>

                      <div className="questions-section">
                        <h3 className="section-subheading">Wellbeing & Support</h3>
                        {QUESTIONS.filter(q => q.section === 'wellbeing').map(question => (
                          <RatingCommentDisplay
                            key={question.id}
                            question={question}
                            value={viewedSubmission.responses?.[question.id]}
                          />
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {managerTab === 'team_health' && viewedSubmission && (
                <div className="tab-content" data-testid="health-submission-detail">
                  <div className="submission-detail">
                    <button 
                      className="btn-back" 
                      onClick={() => setViewedSubmission(null)} 
                      data-testid="back-from-health-detail"
                    >
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M19 12H5M12 19l-7-7 7-7"/>
                      </svg>
                      Back to history
                    </button>

                    <div className="submission-detail-header">
                      <Avatar name={members.find(m => m._id === viewedSubmission.member_id)?.name || 'Unknown'} size={56} />
                      <div>
                        <h2 className="submission-detail-name">{members.find(m => m._id === viewedSubmission.member_id)?.name || 'Unknown'}</h2>
                        <div className="submission-detail-date">{formatDateLong(viewedSubmission.date)}</div>
                      </div>
                    </div>

                    <div className="submission-detail-content">
                      <div className="questions-section">
                        <h3 className="section-subheading">Performance & Progress</h3>
                        {QUESTIONS.filter(q => q.section === 'performance').map(question => (
                          <RatingCommentDisplay
                            key={question.id}
                            question={question}
                            value={viewedSubmission.responses?.[question.id]}
                          />
                        ))}
                      </div>

                      <div className="questions-section">
                        <h3 className="section-subheading">Wellbeing & Support</h3>
                        {QUESTIONS.filter(q => q.section === 'wellbeing').map(question => (
                          <RatingCommentDisplay
                            key={question.id}
                            question={question}
                            value={viewedSubmission.responses?.[question.id]}
                          />
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {managerTab === 'team_health' && !healthDetailMember && !viewedSubmission && (
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
                          <button
                            key={flag._id}
                            className="flag-card clickable-flag"
                            onClick={() => setHealthDetailMember(member)}
                            data-testid={`flag-${flag._id}`}
                          >
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
                          </button>
                        );
                      })}
                    </div>
                  )}
                </div>
              )}

              {managerTab === 'team_health' && healthDetailMember && !viewedSubmission && (
                <div className="tab-content" data-testid="health-detail-panel">
                  <div className="history-panel">
                    <div className="history-header">
                      <button className="btn-back" onClick={() => setHealthDetailMember(null)} data-testid="back-to-health">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <path d="M19 12H5M12 19l-7-7 7-7"/>
                        </svg>
                        Back
                      </button>
                      <div className="history-member-info">
                        <Avatar name={healthDetailMember.name} size={48} />
                        <div>
                          <div className="history-member-name">{healthDetailMember.name}</div>
                          <div className="history-member-title">{healthDetailMember.title}</div>
                        </div>
                      </div>
                    </div>

                    <div className="history-submissions">
                      <h3 className="history-title">Weekly submissions ({allSubmissions.filter(s => s.member_id === healthDetailMember._id).length} weeks)</h3>
                      
                      <div className="history-list">
                        {allSubmissions
                          .filter(s => s.member_id === healthDetailMember._id)
                          .sort((a, b) => b.date.localeCompare(a.date))
                          .map(submission => (
                            <button
                              key={submission._id}
                              className="history-row"
                              onClick={() => setViewedSubmission(submission)}
                              data-testid={`health-history-row-${submission.date}`}
                            >
                              <div className="history-date">{formatDateLong(submission.date)}</div>
                              <div className="history-row-right">
                                <ScoreChips submission={submission} />
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                  <path d="M5 12h14M12 5l7 7-7 7"/>
                                </svg>
                              </div>
                            </button>
                          ))}
                      </div>
                    </div>
                  </div>
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
                              {(() => {
                                const conf = calculateTrends(memberSubmissions, 'target_confidence');
                                return conf.length > 0 ? (
                                  <div style={{ display: "flex", alignItems: "flex-end", gap: "2px", height: 20, width: conf.length * 12 }}>
                                    {conf.map((v, i) => (
                                      <div key={i} style={{ 
                                        flex: 1, 
                                        borderRadius: "2px 2px 0 0", 
                                        height: `${(v / 5) * 100}%`, 
                                        background: v >= 4 ? "#10B981" : v >= 2 ? "#F59E0B" : "#EF4444",
                                        opacity: i === conf.length - 1 ? 1 : 0.6 
                                      }} />
                                    ))}
                                  </div>
                                ) : <span className="sparkline-empty">—</span>;
                              })()}
                            </div>
                            <div className="metric-row">
                              <span className="metric-label">Wellbeing</span>
                              {(() => {
                                const wellbeing = calculateTrends(memberSubmissions, 'feeling_about_work');
                                return wellbeing.length > 0 ? (
                                  <div style={{ display: "flex", alignItems: "flex-end", gap: "2px", height: 20, width: wellbeing.length * 12 }}>
                                    {wellbeing.map((v, i) => (
                                      <div key={i} style={{ 
                                        flex: 1, 
                                        borderRadius: "2px 2px 0 0", 
                                        height: `${(v / 5) * 100}%`, 
                                        background: v >= 4 ? "#10B981" : v >= 2 ? "#F59E0B" : "#EF4444",
                                        opacity: i === wellbeing.length - 1 ? 1 : 0.6 
                                      }} />
                                    ))}
                                  </div>
                                ) : <span className="sparkline-empty">—</span>;
                              })()}
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

              {managerTab === 'ai_briefing' && (
                <div className="tab-content" data-testid="ai-briefing-content">
                  {!briefing && !briefingLoading && (
                    <div className="briefing-empty">
                      <div className="briefing-empty-icon">✦</div>
                      <h3 className="briefing-empty-title">AI Manager Briefing</h3>
                      <p className="briefing-empty-desc">
                        Generate a personalised briefing based on your team's health scores, risk flags, and recent submissions. 
                        Includes priority actions, conversation starters, and wellbeing activities.
                      </p>
                      <button 
                        className="btn-primary btn-large"
                        onClick={generateBriefing}
                        data-testid="generate-briefing-button"
                      >
                        Generate This Week's Briefing
                      </button>
                    </div>
                  )}

                  {briefingLoading && (
                    <div className="briefing-loading">
                      <div className="briefing-loading-icon">✦</div>
                      <div className="briefing-loading-text">Analysing team data and generating your briefing...</div>
                      <div className="briefing-loading-subtext">
                        Reading {allSubmissions.length} submissions, {flags.filter(f => f.status === 'open').length} active flags
                      </div>
                    </div>
                  )}

                  {briefing && !briefingLoading && (
                    <div className="briefing-content">
                      <div className="briefing-card pulse-card">
                        <div className="briefing-card-header">
                          <span className="briefing-icon">✦</span>
                          <h3>Team Pulse — This Week</h3>
                        </div>
                        <p className="pulse-text">{briefing.team_pulse}</p>
                      </div>

                      <div className="briefing-card">
                        <h3 className="briefing-card-title">Priority Actions</h3>
                        <div className="actions-list">
                          {briefing.priority_actions?.map((action, i) => (
                            <div key={i} className="action-item">
                              <span className={`urgency-badge urgency-${action.urgency}`}>
                                {action.urgency === 'today' ? 'TODAY' : action.urgency === 'this_week' ? 'THIS WEEK' : 'NEXT 1:1'}
                              </span>
                              <div className="action-content">
                                <div className="action-main">
                                  <strong>{action.person}:</strong> {action.action}
                                </div>
                                <div className="action-reason">{action.reason}</div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>

                      <div className="briefing-card">
                        <h3 className="briefing-card-title">Daily Briefing Guide</h3>
                        
                        <div className="briefing-subsection">
                          <h4>Suggested Opening</h4>
                          <div className="opening-quote">"{briefing.daily_briefing?.opening}"</div>
                        </div>

                        <div className="briefing-subsection">
                          <h4>Things to Watch Today</h4>
                          <ul className="watch-list">
                            {briefing.daily_briefing?.watch_items?.map((item, i) => (
                              <li key={i}>{item}</li>
                            ))}
                          </ul>
                        </div>

                        <div className="briefing-subsection">
                          <h4>Conversation Starters</h4>
                          <div className="starters-list">
                            {briefing.daily_briefing?.conversation_starters?.map((starter, i) => (
                              <div key={i} className="starter-item">
                                <strong>{starter.person}:</strong> "{starter.starter}"
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>

                      <div className="briefing-two-col">
                        <div className="briefing-card">
                          <h3 className="briefing-card-title">Wellbeing Activities</h3>
                          <div className="activities-list">
                            {briefing.wellbeing_activities?.map((activity, i) => (
                              <div key={i} className="activity-item">
                                <div className="activity-name">{activity.activity}</div>
                                <div className="activity-meta">
                                  <span className="activity-target">{activity.target}</span>
                                  <span className="activity-duration">{activity.duration}</span>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>

                        <div className="briefing-card">
                          <h3 className="briefing-card-title">Recognition</h3>
                          <div className="recognition-list">
                            {briefing.recognition?.map((rec, i) => (
                              <div key={i} className="recognition-item">
                                <div className="recognition-person">{rec.person}</div>
                                <div className="recognition-what">{rec.what}</div>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>

                      <div className="briefing-card risks-card">
                        <div className="briefing-card-header">
                          <span className="briefing-icon">⚑</span>
                          <h3>Risks If No Action Taken</h3>
                        </div>
                        <div className="risks-list">
                          {briefing.risks_to_watch?.map((risk, i) => (
                            <div key={i} className="risk-item">
                              <div className="risk-person">{risk.person}</div>
                              <div className="risk-text">{risk.risk}</div>
                              <div className="risk-timeframe">{risk.timeframe}</div>
                            </div>
                          ))}
                        </div>
                      </div>

                      <div className="briefing-actions">
                        <button 
                          className="btn-secondary"
                          onClick={() => { setBriefing(null); generateBriefing(); }}
                          data-testid="regenerate-briefing-button"
                        >
                          Regenerate Briefing
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              )}

              {managerTab === 'coaching' && (
                <div className="tab-content" data-testid="coaching-content">
                  <div className="coaching-privacy-badge" data-testid="privacy-badge">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z"/>
                    </svg>
                    Private — only visible to you
                  </div>

                  {!coaching && !coachingLoading && (
                    <div className="briefing-empty">
                      <div className="briefing-empty-icon">✨</div>
                      <h3 className="briefing-empty-title">Personal Manager Coaching</h3>
                      <p className="briefing-empty-desc">
                        Get honest, data-driven coaching on how you're responding to your team's wellbeing signals. 
                        This is your private space — no one else can see this coaching.
                      </p>
                      <button 
                        className="btn-primary btn-large"
                        onClick={generateCoaching}
                        data-testid="generate-coaching-button"
                      >
                        Generate Coaching
                      </button>
                    </div>
                  )}

                  {coachingLoading && (
                    <div className="briefing-loading">
                      <div className="briefing-loading-icon">✨</div>
                      <div className="briefing-loading-text">Analysing your management response...</div>
                      <div className="briefing-loading-subtext">
                        Reviewing {flags.filter(f => f.status === 'open').length} open flags, team trends, and action patterns
                      </div>
                    </div>
                  )}

                  {coaching && !coachingLoading && (
                    <div className="coaching-content">
                      <div className="coaching-card coaching-summary">
                        <h3 className="coaching-card-title">How You're Doing</h3>
                        <p className="coaching-summary-text">{coaching.coaching_summary}</p>
                      </div>

                      <div className="coaching-card coaching-strengths">
                        <h3 className="coaching-card-title">What You're Doing Well</h3>
                        <ul className="coaching-list">
                          {coaching.strengths?.map((strength, i) => (
                            <li key={i} className="coaching-list-item">{strength}</li>
                          ))}
                        </ul>
                      </div>

                      <div className="coaching-card coaching-gaps">
                        <h3 className="coaching-card-title">Where to Focus</h3>
                        {coaching.gaps?.map((gap, i) => (
                          <div key={i} className="gap-item">
                            <div className="gap-issue">{gap.issue}</div>
                            <div className="gap-impact">Impact: {gap.impact}</div>
                            <div className="gap-suggestion">→ {gap.suggestion}</div>
                          </div>
                        ))}
                      </div>

                      {coaching.overdue_actions && coaching.overdue_actions.length > 0 && (
                        <div className="coaching-card coaching-overdue">
                          <h3 className="coaching-card-title">Overdue Conversations</h3>
                          {coaching.overdue_actions.map((action, i) => (
                            <div key={i} className="overdue-item">
                              <div className="overdue-header">
                                <span className="overdue-person">{action.person}</span>
                                <span className="overdue-days">{action.days_open} days open</span>
                              </div>
                              <div className="overdue-flag">{action.flag}</div>
                              <div className="overdue-script">
                                <div className="script-label">Conversation opener:</div>
                                <div className="script-text">"{action.script}"</div>
                              </div>
                            </div>
                          ))}
                        </div>
                      )}

                      <div className="coaching-two-col">
                        <div className="coaching-card coaching-skills">
                          <h3 className="coaching-card-title">Skill Development</h3>
                          {coaching.skill_building?.map((skill, i) => (
                            <div key={i} className="skill-item">
                              <div className="skill-name">{skill.skill}</div>
                              <div className="skill-why">{skill.why}</div>
                              <div className="skill-practice">This week: {skill.practice}</div>
                            </div>
                          ))}
                        </div>

                        <div className="coaching-card coaching-challenge">
                          <h3 className="coaching-card-title">This Week's Challenge</h3>
                          <div className="challenge-text">{coaching.weekly_challenge}</div>
                        </div>
                      </div>

                      <div className="briefing-actions">
                        <button 
                          className="btn-secondary"
                          onClick={() => { setCoaching(null); generateCoaching(); }}
                          data-testid="regenerate-coaching-button"
                        >
                          Regenerate Coaching
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </section>
        </main>

        {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
      </div>
    );
  }

  // EXECUTIVE VIEW
  if (view === 'executive') {
    const totalAtRisk = orgTeams.reduce((sum, team) => sum + (team.riskMembers || 0), 0);
    const totalFlags = orgTeams.reduce((sum, team) => sum + (team.activeFlags || 0), 0);
    const allAttritionRisks = orgTeams.flatMap(t => 
      (t.attrition || []).map(a => ({ ...a, team: t.name }))
    ).sort((a, b) => b.risk - a.risk);

    return (
      <div className="app-shell">
        <header className="app-header">
          <div className="header-content">
            <h1 className="header-title" data-testid="app-title">PerformOS</h1>
            <div className="header-right">
              <Avatar name={user.name} size={36} />
              <div className="user-info">
                <div className="user-name" data-testid="user-name">{user.name}</div>
                <div className="user-role">{user.title || 'Executive'}</div>
              </div>
              <button className="btn-secondary btn-sm" onClick={handleLogout} data-testid="logout-button">Sign out</button>
            </div>
          </div>
        </header>

        <main className="main-content">
          <section className="hero-section">
            <h2 className="section-title" data-testid="exec-title">Organization Health</h2>
            <p className="section-subtitle">Real-time team health monitoring and attrition risk tracking across all teams.</p>
          </section>

          <section className="content-section light">
            <div className="content-container">
              <div className="exec-summary-row">
                <div className="exec-kpi">
                  <div className="exec-kpi-value">{orgTeams.length}</div>
                  <div className="exec-kpi-label">Teams</div>
                </div>
                <div className="exec-kpi">
                  <div className="exec-kpi-value" style={{ color: totalFlags > 5 ? '#EF4444' : totalFlags > 0 ? '#F59E0B' : '#10B981' }}>
                    {totalFlags}
                  </div>
                  <div className="exec-kpi-label">Active Flags</div>
                </div>
                <div className="exec-kpi">
                  <div className="exec-kpi-value" style={{ color: totalAtRisk > 2 ? '#EF4444' : totalAtRisk > 0 ? '#F59E0B' : '#10B981' }}>
                    {totalAtRisk}
                  </div>
                  <div className="exec-kpi-label">At Risk</div>
                </div>
              </div>

              <h3 className="section-heading" style={{ marginTop: '3rem' }}>Organization Heatmap</h3>
              <p className="section-description" style={{ marginBottom: '1.5rem' }}>
                Teams sorted by health score (worst-first). Click manager names to view team details. Engineering uses live data.
              </p>

              {!selectedTeam && (
                <div className="org-heatmap">
                  {orgTeams.map(team => {
                    const healthColor = team.health >= 80 ? '#10B981' : team.health >= 60 ? '#06B6D4' : team.health >= 40 ? '#F59E0B' : '#EF4444';
                    const trend5Weeks = team.trend || [];
                    const trendDirection = trend5Weeks.length >= 2 ? 
                      (trend5Weeks[trend5Weeks.length - 1] > trend5Weeks[0] ? 'up' : 
                      trend5Weeks[trend5Weeks.length - 1] < trend5Weeks[0] ? 'down' : 'stable') : 'stable';
                    
                    return (
                      <div key={team.id} className="heatmap-row" data-testid={`heatmap-${team.id}`}>
                        <div className="heatmap-team">
                          <div className="heatmap-team-name">{team.name}</div>
                          <div className="heatmap-team-manager">
                            <button 
                              className="manager-link"
                              onClick={() => setSelectedTeam(team)}
                              data-testid={`manager-link-${team.id}`}
                            >
                              {team.manager}
                            </button>
                            {' · '}{team.headcount} people
                          </div>
                        </div>
                      
                      <div className="heatmap-health">
                        <div 
                          className="heatmap-health-score" 
                          style={{ 
                            background: healthColor,
                            color: 'white',
                            fontWeight: 700
                          }}
                        >
                          {team.health}
                        </div>
                        <div className="heatmap-health-trend">
                          {trendDirection === 'up' && <span style={{ color: '#10B981' }}>↗ improving</span>}
                          {trendDirection === 'down' && <span style={{ color: '#EF4444' }}>↘ declining</span>}
                          {trendDirection === 'stable' && <span style={{ color: '#64748B' }}>→ stable</span>}
                        </div>
                      </div>

                      <div className="heatmap-metrics">
                        <div className="heatmap-metric">
                          <span className="heatmap-metric-value" style={{ color: team.activeFlags > 2 ? '#EF4444' : team.activeFlags > 0 ? '#F59E0B' : '#64748B' }}>
                            {team.activeFlags || 0}
                          </span>
                          <span className="heatmap-metric-label">flags</span>
                        </div>
                        <div className="heatmap-metric">
                          <span className="heatmap-metric-value" style={{ color: team.riskMembers > 0 ? '#EF4444' : '#64748B' }}>
                            {team.riskMembers || 0}
                          </span>
                          <span className="heatmap-metric-label">at risk</span>
                        </div>
                      </div>

                      <div className="heatmap-mini-trend">
                        {trend5Weeks.map((val, i) => (
                          <div 
                            key={i}
                            className="heatmap-bar"
                            style={{
                              height: `${(val / 100) * 36}px`,
                              background: val >= 80 ? '#10B981' : val >= 60 ? '#06B6D4' : val >= 40 ? '#F59E0B' : '#EF4444',
                              opacity: i === trend5Weeks.length - 1 ? 1 : 0.6
                            }}
                          />
                        ))}
                      </div>
                    </div>
                  );
                })}
              </div>
              )}

              {selectedTeam && (
                <div className="team-detail-panel">
                  <button className="btn-back" onClick={() => setSelectedTeam(null)} data-testid="back-to-heatmap">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M19 12H5M12 19l-7-7 7-7"/>
                    </svg>
                    Back to heatmap
                  </button>

                  <div className="team-detail-header">
                    <h3 className="team-detail-title">{selectedTeam.name} — {selectedTeam.manager}'s team</h3>
                    <p className="team-detail-subtitle">
                      {selectedTeam.headcount} members · Aggregated team scores (no individual data)
                    </p>
                  </div>

                  <div className="team-detail-content">
                    <div className="team-detail-metrics">
                      <div className="team-detail-metric">
                        <div className="team-detail-metric-value" style={{ 
                          color: selectedTeam.health >= 80 ? '#10B981' : selectedTeam.health >= 60 ? '#06B6D4' : selectedTeam.health >= 40 ? '#F59E0B' : '#EF4444'
                        }}>
                          {selectedTeam.health}
                        </div>
                        <div className="team-detail-metric-label">Team Health Score</div>
                      </div>
                      <div className="team-detail-metric">
                        <div className="team-detail-metric-value" style={{ color: selectedTeam.activeFlags > 0 ? '#EF4444' : '#10B981' }}>
                          {selectedTeam.activeFlags}
                        </div>
                        <div className="team-detail-metric-label">Active Flags</div>
                      </div>
                      <div className="team-detail-metric">
                        <div className="team-detail-metric-value" style={{ color: selectedTeam.riskMembers > 0 ? '#EF4444' : '#10B981' }}>
                          {selectedTeam.riskMembers}
                        </div>
                        <div className="team-detail-metric-label">Members At Risk</div>
                      </div>
                    </div>

                    {selectedTeam.attrition && selectedTeam.attrition.length > 0 && (
                      <div className="team-detail-section">
                        <h4 className="team-detail-section-title">Attrition Risks</h4>
                        {selectedTeam.attrition.map((risk, i) => (
                          <div key={i} className="attrition-card">
                            <div className="attrition-header">
                              <div className="attrition-role">
                                <div className="attrition-role-title">{risk.role}</div>
                              </div>
                              <div 
                                className="attrition-risk-score"
                                style={{
                                  background: `rgba(${risk.risk >= 70 ? '239, 68, 68' : '245, 158, 11'}, 0.1)`,
                                  color: risk.risk >= 70 ? '#EF4444' : '#F59E0B',
                                  border: `2px solid ${risk.risk >= 70 ? '#EF4444' : '#F59E0B'}`
                                }}
                              >
                                {risk.risk}% flight risk
                              </div>
                            </div>
                            <div className="attrition-reason">{risk.reason}</div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              )}

              {!selectedTeam && allAttritionRisks.length > 0 && (
                <>
                  <h3 className="section-heading" style={{ marginTop: '3rem' }}>Attrition Risks</h3>
                  <p className="section-description" style={{ marginBottom: '1.5rem' }}>
                    Team members showing elevated flight risk based on wellbeing scores, flag patterns, and engagement trends. 
                    Role titles shown for privacy.
                  </p>

                  <div className="attrition-list">
                    {allAttritionRisks.map((risk, i) => {
                      const riskLevel = risk.risk >= 70 ? 'critical' : risk.risk >= 50 ? 'high' : 'moderate';
                      const riskColor = riskLevel === 'critical' ? '#EF4444' : riskLevel === 'high' ? '#F59E0B' : '#F59E0B';
                      
                      return (
                        <div key={i} className="attrition-card" data-testid={`attrition-${i}`}>
                          <div className="attrition-header">
                            <div className="attrition-role">
                              <div className="attrition-role-title">{risk.role}</div>
                              <div className="attrition-role-team">{risk.team}</div>
                            </div>
                            <div 
                              className="attrition-risk-score"
                              style={{
                                background: `rgba(${riskLevel === 'critical' ? '239, 68, 68' : '245, 158, 11'}, 0.1)`,
                                color: riskColor,
                                border: `2px solid ${riskColor}`
                              }}
                            >
                              {risk.risk}% flight risk
                            </div>
                          </div>
                          <div className="attrition-reason">{risk.reason}</div>
                        </div>
                      );
                    })}
                  </div>

                  <div className="replacement-cost-banner">
                    <div className="replacement-cost-icon">⚠️</div>
                    <div className="replacement-cost-content">
                      <div className="replacement-cost-title">Elevated Flight Risk</div>
                      <div className="replacement-cost-text">
                        {totalAtRisk} team members across {orgTeams.filter(t => t.riskMembers > 0).length} teams show elevated flight risk signals based on declining scores, unresolved flags, and behavioural patterns.
                      </div>
                    </div>
                  </div>
                </>
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
