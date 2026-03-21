#!/usr/bin/env python3
"""
PerformOS One-on-One Builder V2 - Backend API Testing
Tests all V2 API endpoints with manager and team member credentials
"""

import requests
import sys
import json
from datetime import datetime

class PerformOSV2APITester:
    def __init__(self, base_url="https://team-health-hub-2.preview.emergentagent.com"):
        self.base_url = base_url
        self.manager_token = None
        self.team_member_token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []

    def log_test(self, name, success, details=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name}")
        else:
            print(f"❌ {name} - {details}")
            self.failed_tests.append(f"{name}: {details}")

    def make_request(self, method, endpoint, token=None, data=None, expected_status=200):
        """Make API request with error handling"""
        url = f"{self.base_url}{endpoint}"
        headers = {'Content-Type': 'application/json'}
        if token:
            headers['Authorization'] = f'Bearer {token}'

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method == 'PATCH':
                response = requests.patch(url, json=data, headers=headers, timeout=10)
            else:
                return False, f"Unsupported method: {method}"

            success = response.status_code == expected_status
            if success:
                try:
                    return True, response.json()
                except:
                    return True, {}
            else:
                return False, f"Status {response.status_code}: {response.text[:200]}"
        except Exception as e:
            return False, str(e)

    def test_connectivity(self):
        """Test basic API connectivity"""
        success, result = self.make_request('GET', '/')
        if success and isinstance(result, dict) and 'message' in result:
            self.log_test("Backend API connectivity", True)
            return True
        else:
            self.log_test("Backend API connectivity", False, result)
            return False

    def test_manager_login(self):
        """Test manager login"""
        success, result = self.make_request(
            'POST', 
            '/api/auth/login',
            data={"email": "alex@performos.io", "password": "demo"}
        )
        
        if success and isinstance(result, dict) and 'access_token' in result:
            self.manager_token = result['access_token']
            user = result.get('user', {})
            if user.get('role') == 'manager':
                self.log_test("Manager login", True)
                return True
            else:
                self.log_test("Manager login", False, f"Expected manager role, got: {user.get('role')}")
                return False
        else:
            self.log_test("Manager login", False, result)
            return False

    def test_team_member_login(self):
        """Test team member login"""
        success, result = self.make_request(
            'POST', 
            '/api/auth/login',
            data={"email": "sarah@performos.io", "password": "demo"}
        )
        
        if success and isinstance(result, dict) and 'access_token' in result:
            self.team_member_token = result['access_token']
            user = result.get('user', {})
            if user.get('role') == 'team_member':
                self.log_test("Team member login", True)
                return True
            else:
                self.log_test("Team member login", False, f"Expected team_member role, got: {user.get('role')}")
                return False
        else:
            self.log_test("Team member login", False, result)
            return False

    def test_manager_auth_me(self):
        """Test manager auth/me endpoint"""
        success, result = self.make_request('GET', '/api/auth/me', token=self.manager_token)
        
        if success and isinstance(result, dict) and result.get('role') == 'manager':
            self.log_test("Manager auth/me", True)
            return True
        else:
            self.log_test("Manager auth/me", False, f"Expected manager role, got: {result}")
            return False

    def test_team_member_auth_me(self):
        """Test team member auth/me endpoint"""
        success, result = self.make_request('GET', '/api/auth/me', token=self.team_member_token)
        
        if success and isinstance(result, dict) and result.get('role') == 'team_member':
            self.log_test("Team member auth/me", True)
            return True
        else:
            self.log_test("Team member auth/me", False, f"Expected team_member role, got: {result}")
            return False

    def test_weekly_schedule(self):
        """Test weekly schedule endpoint"""
        success, result = self.make_request('GET', '/api/schedule/weeks')
        
        if success and isinstance(result, dict):
            weeks = result.get('weeks', [])
            current_week = result.get('current_week')
            if len(weeks) == 15 and current_week == "2026-03-23":
                self.log_test("Weekly schedule (15 Monday dates)", True)
                return True
            else:
                self.log_test("Weekly schedule", False, f"Expected 15 weeks with current week 2026-03-23, got {len(weeks)} weeks, current: {current_week}")
                return False
        else:
            self.log_test("Weekly schedule", False, f"Expected dict, got: {type(result)}")
            return False

    def test_schedule_status(self):
        """Test schedule status for team member"""
        success, result = self.make_request('GET', '/api/schedule/status', token=self.team_member_token)
        
        if success and isinstance(result, list) and len(result) == 15:
            current_week_status = next((s for s in result if s.get('is_current_week')), None)
            if current_week_status and current_week_status.get('date') == "2026-03-23":
                self.log_test("Schedule status (team member)", True)
                return True
            else:
                self.log_test("Schedule status", False, "No current week (2026-03-23) found in status")
                return False
        else:
            self.log_test("Schedule status", False, f"Expected list of 15 items, got: {type(result)} {len(result) if isinstance(result, list) else 'non-list'}")
            return False

    def test_manager_members(self):
        """Test manager members list"""
        success, result = self.make_request('GET', '/api/members', token=self.manager_token)
        
        if success and isinstance(result, list) and len(result) == 6:
            self.log_test("Manager members list (6 team members)", True)
            return True
        else:
            self.log_test("Manager members list", False, f"Expected 6 members, got: {type(result)} {len(result) if isinstance(result, list) else 'non-list'}")
            return False

    def test_manager_dashboard_stats(self):
        """Test manager dashboard stats"""
        success, result = self.make_request('GET', '/api/stats/dashboard', token=self.manager_token)
        
        expected_keys = ['this_week_submissions', 'total_team_members', 'team_health_score', 'active_flags']
        if success and isinstance(result, dict):
            missing_keys = [key for key in expected_keys if key not in result]
            if not missing_keys:
                self.log_test("Manager dashboard stats", True)
                return True
            else:
                self.log_test("Manager dashboard stats", False, f"Missing keys: {missing_keys}")
                return False
        else:
            self.log_test("Manager dashboard stats", False, f"Expected dict, got: {type(result)}")
            return False

    def test_this_week_submissions(self):
        """Test this week submissions for manager"""
        success, result = self.make_request('GET', '/api/this-week/submissions', token=self.manager_token)
        
        if success and isinstance(result, list):
            submitted_count = sum(1 for item in result if item.get('has_submitted'))
            self.log_test(f"This week submissions ({submitted_count}/{len(result)} submitted)", True)
            return True
        else:
            self.log_test("This week submissions", False, f"Expected list, got: {type(result)}")
            return False

    def test_manager_flags(self):
        """Test manager flags list"""
        success, result = self.make_request('GET', '/api/flags?status_filter=open', token=self.manager_token)
        
        if success and isinstance(result, list):
            flag_count = len(result)
            self.log_test(f"Manager flags list ({flag_count} active flags)", True)
            return True
        else:
            self.log_test("Manager flags list", False, f"Expected list, got: {type(result)}")
            return False

    def test_submissions(self):
        """Test submissions endpoint for manager"""
        success, result = self.make_request('GET', '/api/submissions', token=self.manager_token)
        
        if success and isinstance(result, list):
            self.log_test(f"Manager submissions list ({len(result)} total)", True)
            return True
        else:
            self.log_test("Manager submissions list", False, f"Expected list, got: {type(result)}")
            return False

    def test_team_member_members(self):
        """Test team member members list (should return own record)"""
        success, result = self.make_request('GET', '/api/members', token=self.team_member_token)
        
        if success and isinstance(result, list) and len(result) == 1:
            member = result[0]
            if member.get('name') == 'Sarah Mitchell':
                self.log_test("Team member members list (own record)", True)
                return True
            else:
                self.log_test("Team member members list", False, f"Expected Sarah Mitchell, got: {member.get('name')}")
                return False
        else:
            self.log_test("Team member members list", False, f"Expected 1 member, got: {len(result) if isinstance(result, list) else 'non-list'}")
            return False

    def test_team_member_submissions(self):
        """Test team member submissions list"""
        success, result = self.make_request('GET', '/api/submissions', token=self.team_member_token)
        
        if success and isinstance(result, list):
            self.log_test(f"Team member submissions list ({len(result)} submissions)", True)
            return True
        else:
            self.log_test("Team member submissions list", False, result)
            return False

    def test_unauthorized_access(self):
        """Test that endpoints require authentication"""
        success, result = self.make_request('GET', '/api/members', expected_status=401)
        
        if success:
            self.log_test("Unauthorized access protection", True)
            return True
        else:
            self.log_test("Unauthorized access protection", False, "Should require authentication")
            return False

    def run_all_tests(self):
        """Run all API tests"""
        print("🧪 Starting PerformOS One-on-One Builder V2 API Tests")
        print("🌐 Testing against:", self.base_url)
        print("=" * 60)
        
        # Test sequence
        tests = [
            self.test_connectivity,
            self.test_manager_login,
            self.test_team_member_login,
            self.test_manager_auth_me,
            self.test_team_member_auth_me,
            self.test_weekly_schedule,
            self.test_schedule_status,
            self.test_manager_members,
            self.test_manager_dashboard_stats,
            self.test_this_week_submissions,
            self.test_manager_flags,
            self.test_submissions,
            self.test_team_member_members,
            self.test_team_member_submissions,
            self.test_unauthorized_access,
        ]
        
        # Run all tests
        for test in tests:
            try:
                test()
            except Exception as e:
                print(f"❌ Test {test.__name__} failed with exception: {str(e)}")
                self.failed_tests.append(f"{test.__name__}: {str(e)}")
        
        # Print results
        print("\n" + "=" * 60)
        print(f"📊 Test Results: {self.tests_passed}/{self.tests_run} passed")
        
        if self.failed_tests:
            print("\n❌ Failed Tests:")
            for failure in self.failed_tests:
                print(f"   • {failure}")
        else:
            print("\n✅ All tests passed!")
        
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        print(f"\n🎯 Success Rate: {success_rate:.1f}%")
        
        return self.tests_passed == self.tests_run

def main():
    tester = PerformOSV2APITester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())