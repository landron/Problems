#pragma once

/*
   "does not implement any other operations, in particular no equality comparison or arithmetic operators"
   help me found an error:
      Error	1	error C2676: binary '>' : 'const KType' does not define this operator or a conversion to a type acceptable to the predefined operator	f:\devel\extra\problems\various\004-intervalmap\interval_map.h	97	1	think-cell
*/
template<class K>
class CustomK
{
   // copyable and assignable
   K m_val;

public:
   explicit CustomK(const K& val): m_val(val) {}

   bool operator <(const CustomK& other) const {
      return m_val < other.m_val;
   }

   friend static inline
   std::ostream& operator<<(std::ostream& os, const CustomK<K>& obj)
   {
       os << obj.m_val;
       return os;
   }
};

template<class V>
class CustomV
{
   // copyable and assignable
   V m_val;

public:
   explicit CustomV(const V& val): m_val(val) {}

   bool operator ==(const CustomV& other) const {
      return m_val == other.m_val;
   }

   friend static inline
   std::ostream& operator<<(std::ostream& os, const CustomV<V>& obj)
   {
       os << obj.m_val;
       return os;
   }
};

