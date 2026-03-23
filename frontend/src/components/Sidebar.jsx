import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  MessageSquare,
  Upload,
  FileText,
  GraduationCap,
  LogOut,
  Bot,
  ChevronLeft,
} from 'lucide-react';

const NAV_ITEMS = [
  { to: '/', icon: LayoutDashboard, label: '대시보드' },
  { to: '/chat', icon: MessageSquare, label: 'AI 채팅' },
  { to: '/upload', icon: Upload, label: '문서 업로드' },
  { to: '/documents', icon: FileText, label: '내 문서' },
  { to: '/quiz', icon: GraduationCap, label: '퀴즈' },
];

export default function Sidebar({ collapsed, onToggle, onSignOut }) {
  return (
    <aside className={`sidebar ${collapsed ? 'sidebar--collapsed' : ''}`}>
      {/* Brand */}
      <div className="sidebar__brand">
        <Bot size={28} className="sidebar__logo" />
        {!collapsed && <span className="sidebar__title">StudyBot</span>}
        <button className="sidebar__toggle" onClick={onToggle} aria-label="사이드바 토글">
          <ChevronLeft size={18} />
        </button>
      </div>

      {/* Navigation */}
      <nav className="sidebar__nav">
        {NAV_ITEMS.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            className={({ isActive }) =>
              `sidebar__link ${isActive ? 'sidebar__link--active' : ''}`
            }
            title={label}
          >
            <Icon size={20} />
            {!collapsed && <span>{label}</span>}
          </NavLink>
        ))}
      </nav>

      {/* Sign out */}
      <div className="sidebar__footer">
        <button className="sidebar__link sidebar__signout" onClick={onSignOut}>
          <LogOut size={20} />
          {!collapsed && <span>로그아웃</span>}
        </button>
      </div>
    </aside>
  );
}
