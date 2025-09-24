import { NavLink } from 'react-router-dom';

const navigationItems = [
  { name: 'Dashboard', href: '/', icon: '📊' },
  { name: 'LinkedIn Posts', href: '/posts', icon: '📝' },
  { name: 'Opportunities', href: '/opportunities', icon: '🎯' },
  { name: 'Proposals', href: '/proposals', icon: '📄' },
  { name: 'Campaigns', href: '/campaigns', icon: '📢' },
  { name: 'Companies', href: '/companies', icon: '🏢' },
  { name: 'Contacts', href: '/contacts', icon: '👥' },
  { name: 'Settings', href: '/settings', icon: '⚙️' },
];

function Sidebar({ isOpen, onClose }) {
  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-gray-600 bg-opacity-75 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <div className={`
        fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0
        ${isOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        <div className="flex flex-col h-full">
          {/* Logo area */}
          <div className="flex items-center justify-between px-4 py-6 border-b">
            <div className="flex items-center">
              <span className="text-xl font-bold text-gray-900">MapMyClient</span>
            </div>
            <button
              onClick={onClose}
              className="lg:hidden p-2 rounded-md text-gray-400 hover:text-gray-600"
            >
              <span className="sr-only">Close sidebar</span>
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-4 py-6 space-y-1">
            {navigationItems.map((item) => (
              <NavLink
                key={item.name}
                to={item.href}
                className={({ isActive }) =>
                  `flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors ${
                    isActive
                      ? 'bg-blue-50 text-blue-600 border-r-2 border-blue-600'
                      : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                  }`
                }
                onClick={() => onClose()}
              >
                <span className="mr-3 text-lg">{item.icon}</span>
                {item.name}
              </NavLink>
            ))}
          </nav>

          {/* Footer */}
          <div className="px-4 py-4 border-t">
            <p className="text-xs text-gray-500">
              Version 1.0.0 • MapMyClient
            </p>
          </div>
        </div>
      </div>
    </>
  );
}

export default Sidebar;