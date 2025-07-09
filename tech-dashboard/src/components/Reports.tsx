import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  FileText, 
  Download, 
  Calendar, 
  Filter,
  Search,
  Eye,
  MoreHorizontal,
  TrendingUp,
  TrendingDown,
  DollarSign,
  Users,
  ShoppingCart
} from 'lucide-react';

const Reports: React.FC = () => {
  const [selectedReport, setSelectedReport] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  const reportTypes = [
    { id: 'all', name: 'All Reports', count: 24 },
    { id: 'financial', name: 'Financial', count: 8 },
    { id: 'user', name: 'User Analytics', count: 6 },
    { id: 'sales', name: 'Sales', count: 5 },
    { id: 'performance', name: 'Performance', count: 5 },
  ];

  const reports = [
    {
      id: 1,
      title: 'Monthly Revenue Report',
      type: 'financial',
      description: 'Comprehensive monthly revenue analysis with trends and projections',
      date: '2024-01-15',
      size: '2.4 MB',
      downloads: 156,
      status: 'published',
      icon: DollarSign,
      color: 'text-green-600',
      bgColor: 'bg-green-50'
    },
    {
      id: 2,
      title: 'User Engagement Analytics',
      type: 'user',
      description: 'Detailed user behavior and engagement metrics for Q4 2023',
      date: '2024-01-12',
      size: '1.8 MB',
      downloads: 89,
      status: 'published',
      icon: Users,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50'
    },
    {
      id: 3,
      title: 'Sales Performance Dashboard',
      type: 'sales',
      description: 'Sales team performance and conversion rate analysis',
      date: '2024-01-10',
      size: '3.1 MB',
      downloads: 234,
      status: 'published',
      icon: ShoppingCart,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50'
    },
    {
      id: 4,
      title: 'System Performance Report',
      type: 'performance',
      description: 'Infrastructure and application performance metrics',
      date: '2024-01-08',
      size: '1.2 MB',
      downloads: 67,
      status: 'draft',
      icon: TrendingUp,
      color: 'text-orange-600',
      bgColor: 'bg-orange-50'
    },
    {
      id: 5,
      title: 'Customer Satisfaction Survey',
      type: 'user',
      description: 'Q4 customer satisfaction and feedback analysis',
      date: '2024-01-05',
      size: '0.9 MB',
      downloads: 123,
      status: 'published',
      icon: Users,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50'
    },
    {
      id: 6,
      title: 'Annual Financial Summary',
      type: 'financial',
      description: 'Complete annual financial performance and projections',
      date: '2024-01-01',
      size: '4.7 MB',
      downloads: 445,
      status: 'published',
      icon: DollarSign,
      color: 'text-green-600',
      bgColor: 'bg-green-50'
    }
  ];

  const filteredReports = reports.filter(report => {
    const matchesType = selectedReport === 'all' || report.type === selectedReport;
    const matchesSearch = report.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         report.description.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesType && matchesSearch;
  });

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'published':
        return 'bg-green-100 text-green-800';
      case 'draft':
        return 'bg-yellow-100 text-yellow-800';
      case 'archived':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Reports</h1>
          <p className="text-gray-600">Generate and manage business reports</p>
        </div>
        <button className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
          <FileText className="w-4 h-4" />
          <span>Generate Report</span>
        </button>
      </div>

      {/* Filters and Search */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
          {/* Report Type Filter */}
          <div className="flex flex-wrap gap-2">
            {reportTypes.map((type) => (
              <button
                key={type.id}
                onClick={() => setSelectedReport(type.id)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  selectedReport === type.id
                    ? 'bg-blue-100 text-blue-700'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {type.name} ({type.count})
              </button>
            ))}
          </div>

          {/* Search */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search reports..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent w-64"
            />
          </div>
        </div>
      </div>

      {/* Reports Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredReports.map((report, index) => {
          const Icon = report.icon;
          return (
            <motion.div
              key={report.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between mb-4">
                <div className={`p-3 rounded-lg ${report.bgColor}`}>
                  <Icon className={`w-6 h-6 ${report.color}`} />
                </div>
                <div className="flex items-center space-x-2">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(report.status)}`}>
                    {report.status}
                  </span>
                  <button className="p-1 rounded-md text-gray-400 hover:text-gray-600 hover:bg-gray-100">
                    <MoreHorizontal className="w-4 h-4" />
                  </button>
                </div>
              </div>

              <h3 className="text-lg font-semibold text-gray-900 mb-2">{report.title}</h3>
              <p className="text-sm text-gray-600 mb-4 line-clamp-2">{report.description}</p>

              <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                <div className="flex items-center space-x-2">
                  <Calendar className="w-4 h-4" />
                  <span>{new Date(report.date).toLocaleDateString()}</span>
                </div>
                <span>{report.size}</span>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2 text-sm text-gray-500">
                  <Download className="w-4 h-4" />
                  <span>{report.downloads} downloads</span>
                </div>
                <div className="flex items-center space-x-2">
                  <button className="p-2 rounded-md text-gray-400 hover:text-gray-600 hover:bg-gray-100">
                    <Eye className="w-4 h-4" />
                  </button>
                  <button className="p-2 rounded-md text-gray-400 hover:text-gray-600 hover:bg-gray-100">
                    <Download className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Reports</p>
              <p className="text-2xl font-bold text-gray-900">24</p>
            </div>
            <div className="p-3 rounded-lg bg-blue-50">
              <FileText className="w-6 h-6 text-blue-600" />
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.9 }}
          className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Published</p>
              <p className="text-2xl font-bold text-gray-900">18</p>
            </div>
            <div className="p-3 rounded-lg bg-green-50">
              <TrendingUp className="w-6 h-6 text-green-600" />
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.0 }}
          className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Drafts</p>
              <p className="text-2xl font-bold text-gray-900">6</p>
            </div>
            <div className="p-3 rounded-lg bg-yellow-50">
              <FileText className="w-6 h-6 text-yellow-600" />
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.1 }}
          className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Downloads</p>
              <p className="text-2xl font-bold text-gray-900">1,114</p>
            </div>
            <div className="p-3 rounded-lg bg-purple-50">
              <Download className="w-6 h-6 text-purple-600" />
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Reports; 