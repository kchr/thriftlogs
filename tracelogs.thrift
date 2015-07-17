struct CreateBucketRequest {
  1: required string name
}

struct CreateBucketResponse {
  1: required string token
}

struct GetTracesRequest {
  1: required string token
  2: optional string type
}

struct Trace {
  1: required string type
  2: optional string message
  3: optional list<string> stack
  4: optional string context // JSON encoded string since thrift cannot communicate unstructured data
}

struct GetTracesResponse {
  1: required list<Trace> traces
}

service TraceLogService {
  CreateBucketResponse createBucket(1: CreateBucketRequest request)
  GetTracesResponse getTraces(1: GetTracesRequest request)
}
