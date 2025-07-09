import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Menu, 
  Search, 
  Bell, 
  Settings, 
  User, 
  LogOut,
  ChevronDown,
  Calendar,
  Clock
} from 'lucide-react';

interface HeaderProps {
  onMenuClick: () => void;
  currentView: string;
}

const Header: React.FC<HeaderProps> = ({ onMenuClick, currentView }) => {
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);

  const getViewTitle = (view: string) => {
    switch (view) {
      case 'dashboard': return 'Dashboard';
      case 'analytics': return 'Analytics';
      case 'reports': return 'Reports';
      case 'settings': return 'Settings';
      default: return 'Dashboard';
    }
  };

  const notifications = [
    { id: 1, message: 'New user registration', time: '2 min ago', type: 'info' },
    { id: 2, message: 'Revenue target achieved', time: '1 hour ago', type: 'success' },
    { id: 3, message: 'System maintenance scheduled', time: '3 hours ago', type: 'warning' },
  ];

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="flex items-center justify-between h-16 px-6">
        {/* Left side */}
        <div className="flex items-center space-x-4">
          <button
            onClick={onMenuClick}
            className="lg:hidden p-2 rounded-md text-gray-400 hover:text-gray-600 hover:bg-gray-100"
          >
            <Menu className="w-5 h-5" />
          </button>
          
          <div className="hidden lg:block">
            <h1 className="text-2xl font-bold text-gray-900">{getViewTitle(currentView)}</h1>
            <p className="text-sm text-gray-500">Welcome back, John</p>
          </div>
        </div>

        {/* Center - Search */}
        <div className="flex-1 max-w-lg mx-8 hidden md:block">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search analytics, reports, users..."
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>

        {/* Right side */}
        <div className="flex items-center space-x-4">
          {/* Date/Time */}
          <div className="hidden sm:flex items-center space-x-2 text-sm text-gray-500">
            <Calendar className="w-4 h-4" />
            <span>{new Date().toLocaleDateString()}</span>
            <Clock className="w-4 h-4 ml-2" />
            <span>{new Date().toLocaleTimeString()}</span>
          </div>

          {/* Notifications */}
          <div className="relative">
            <button
              onClick={() => setShowNotifications(!showNotifications)}
              className="relative p-2 rounded-md text-gray-400 hover:text-gray-600 hover:bg-gray-100"
            >
              <Bell className="w-5 h-5" />
              <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
            </button>

            {showNotifications && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg border border-gray-200 z-50"
              >
                <div className="p-4 border-b border-gray-200">
                  <h3 className="text-lg font-semibold text-gray-900">Notifications</h3>
                </div>
                <div className="max-h-64 overflow-y-auto">
                  {notifications.map((notification) => (
                    <div key={notification.id} className="p-4 border-b border-gray-100 hover:bg-gray-50">
                      <p className="text-sm font-medium text-gray-900">{notification.message}</p>
                      <p className="text-xs text-gray-500 mt-1">{notification.time}</p>
                    </div>
                  ))}
                </div>
                <div className="p-4">
                  <button className="w-full text-sm text-blue-600 hover:text-blue-700 font-medium">
                    View all notifications
                  </button>
                </div>
              </motion.div>
            )}
          </div>

          {/* User Menu */}
          <div className="relative">
            <button
              onClick={() => setShowUserMenu(!showUserMenu)}
              className="flex items-center space-x-2 p-2 rounded-md text-gray-400 hover:text-gray-600 hover:bg-gray-100"
            >
              <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center">
                <span className="text-white text-sm font-medium">JD</span>
              </div>
              <span className="hidden sm:block text-sm font-medium text-gray-700">John Doe</span>
              <ChevronDown className="w-4 h-4" />
            </button>

            {showUserMenu && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-50"
              >
                <div className="py-1">
                  <button className="w-full flex items-center space-x-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                    <User className="w-4 h-4" />
                    <span>Profile</span>
                  </button>
                  <button className="w-full flex items-center space-x-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                    <Settings className="w-4 h-4" />
                    <span>Settings</span>
                  </button>
                  <hr className="my-1" />
                  <button className="w-full flex items-center space-x-2 px-4 py-2 text-sm text-red-600 hover:bg-red-50">
                    <LogOut className="w-4 h-4" />
                    <span>Sign out</span>
                  </button>
                </div>
              </motion.div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header; 