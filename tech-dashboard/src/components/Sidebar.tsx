import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  LayoutDashboard, 
  BarChart3, 
  FileText, 
  Settings, 
  X,
  TrendingUp,
  Users,
  ShoppingCart,
  Activity
} from 'lucide-react';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
  currentView: string;
  onViewChange: (view: string) => void;
}

const navigationItems = [
  { id: 'dashboard', name: 'Dashboard', icon: LayoutDashboard, color: 'text-blue-600' },
  { id: 'analytics', name: 'Analytics', icon: BarChart3, color: 'text-green-600' },
  { id: 'reports', name: 'Reports', icon: FileText, color: 'text-purple-600' },
  { id: 'settings', name: 'Settings', icon: Settings, color: 'text-gray-600' },
];

const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose, currentView, onViewChange }) => {
  return (
    <>
      {/* Mobile overlay */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
            onClick={onClose}
          />
        )}
      </AnimatePresence>

      {/* Sidebar */}
      <motion.div
        initial={{ x: -300 }}
        animate={{ x: isOpen ? 0 : -300 }}
        transition={{ type: "spring", damping: 25, stiffness: 200 }}
        className={`fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-xl lg:static lg:inset-0 ${
          isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        {/* Header */}
        <div className="flex items-center justify-between h-16 px-6 border-b border-gray-200">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
              <Activity className="w-5 h-5 text-white" />
            </div>
            <h1 className="text-xl font-bold text-gray-900">DataViz Pro</h1>
          </div>
          <button
            onClick={onClose}
            className="lg:hidden p-2 rounded-md text-gray-400 hover:text-gray-600 hover:bg-gray-100"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Navigation */}
        <nav className="mt-8 px-4">
          <div className="space-y-2">
            {navigationItems.map((item) => {
              const Icon = item.icon;
              const isActive = currentView === item.id;
              
              return (
                <motion.button
                  key={item.id}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => onViewChange(item.id)}
                  className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-left transition-all duration-200 ${
                    isActive
                      ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-600'
                      : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                  }`}
                >
                  <Icon className={`w-5 h-5 ${isActive ? 'text-blue-600' : item.color}`} />
                  <span className="font-medium">{item.name}</span>
                </motion.button>
              );
            })}
          </div>
        </nav>

        {/* Quick Stats */}
        <div className="mt-8 px-4">
          <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-4">
            Quick Stats
          </h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
              <div className="flex items-center space-x-2">
                <TrendingUp className="w-4 h-4 text-green-600" />
                <span className="text-sm font-medium text-green-700">Revenue</span>
              </div>
              <span className="text-sm font-bold text-green-700">+12.5%</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
              <div className="flex items-center space-x-2">
                <Users className="w-4 h-4 text-blue-600" />
                <span className="text-sm font-medium text-blue-700">Users</span>
              </div>
              <span className="text-sm font-bold text-blue-700">+8.2%</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-purple-50 rounded-lg">
              <div className="flex items-center space-x-2">
                <ShoppingCart className="w-4 h-4 text-purple-600" />
                <span className="text-sm font-medium text-purple-700">Orders</span>
              </div>
              <span className="text-sm font-bold text-purple-700">+15.3%</span>
            </div>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="mt-6 px-4">
          <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-4">
            Recent Activity
          </h3>
          <div className="space-y-3">
            <div className="flex items-start space-x-3">
              <div className="w-2 h-2 bg-green-500 rounded-full mt-2"></div>
              <div className="flex-1 min-w-0">
                <p className="text-xs text-gray-900 font-medium">New user registered</p>
                <p className="text-xs text-gray-500">2 minutes ago</p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <div className="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
              <div className="flex-1 min-w-0">
                <p className="text-xs text-gray-900 font-medium">Revenue target achieved</p>
                <p className="text-xs text-gray-500">1 hour ago</p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <div className="w-2 h-2 bg-purple-500 rounded-full mt-2"></div>
              <div className="flex-1 min-w-0">
                <p className="text-xs text-gray-900 font-medium">System maintenance</p>
                <p className="text-xs text-gray-500">3 hours ago</p>
              </div>
            </div>
          </div>
        </div>

        {/* User Profile */}
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center">
              <span className="text-white text-sm font-medium">JD</span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">John Doe</p>
              <p className="text-xs text-gray-500 truncate">Administrator</p>
            </div>
          </div>
        </div>
      </motion.div>
    </>
  );
};

export default Sidebar; 