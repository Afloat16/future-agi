import { useState } from "react";
import PropTypes from "prop-types";
import { Box, Collapse, IconButton, Stack, Typography } from "@mui/material";
import Iconify from "src/components/iconify";
import StatusBadge from "src/components/status-badge/StatusBadge";
import { WORKER_COPY as COPY } from "./readiness.constants";

const lineSx = {
  borderTop: "1px solid",
  borderColor: "divider",
  px: 1.5,
  py: 1,
};

const BOUNDARY = {
  allowed: COPY.allowed,
  blocked: COPY.blocked,
  not_enforced: COPY.notEnforced,
};

// The status chip's label: a worker held on its own channel reads cooperative, never enforced.
const statusLabel = (worker) =>
  worker.reason_code === "held_at_world_cooperative"
    ? COPY.heldCooperative
    : worker.name;

function WorkerRow({ worker, dimmed }) {
  const [open, setOpen] = useState(false);
  return (
    <Box
      data-testid="worker-boundary"
      data-worker={worker.worker_id}
      sx={{ ...lineSx, opacity: dimmed ? 0.5 : 1 }}
    >
      <Stack direction="row" spacing={1} alignItems="center">
        <Typography
          sx={{ typography: "s2", fontWeight: "fontWeightSemiBold" }}
          noWrap
        >
          {worker.name}
        </Typography>
        <StatusBadge
          status={worker.status}
          label={statusLabel(worker)}
          variant="dot"
        />
        <Box sx={{ flex: 1 }} />
        <IconButton
          size="small"
          aria-label={
            open ? COPY.hideTools(worker.name) : COPY.showTools(worker.name)
          }
          onClick={() => setOpen((was) => !was)}
        >
          <Iconify
            icon={
              open ? "solar:alt-arrow-up-linear" : "solar:alt-arrow-down-linear"
            }
            width={16}
          />
        </IconButton>
      </Stack>
      <Typography sx={{ typography: "s3", color: "text.secondary" }}>
        {worker.reason}
      </Typography>
      {worker.bypassed?.length > 0 && (
        <Typography sx={{ typography: "s3", color: "warning.dark" }}>
          {COPY.bypassed(worker.bypassed.length)}
        </Typography>
      )}
      {worker.fix && (
        <Typography sx={{ typography: "s3", color: "text.primary" }}>
          {worker.fix.action}
        </Typography>
      )}
      <Collapse in={open} unmountOnExit>
        <Box
          component="table"
          sx={{ mt: 1, width: "100%", borderCollapse: "collapse" }}
        >
          <Box component="thead">
            <Box component="tr">
              {[
                COPY.columns.tool,
                COPY.columns.action,
                COPY.columns.boundary,
              ].map((heading) => (
                <Box
                  component="th"
                  key={heading}
                  sx={{
                    typography: "s3",
                    color: "text.secondary",
                    textAlign: "left",
                    fontWeight: "fontWeightMedium",
                    py: 0.5,
                  }}
                >
                  {heading}
                </Box>
              ))}
            </Box>
          </Box>
          <Box component="tbody">
            {worker.tools.map((tool) => (
              <Box component="tr" key={tool.tool} data-testid="worker-tool">
                <Box component="td" sx={{ typography: "s3", py: 0.25 }}>
                  {tool.tool}
                </Box>
                <Box
                  component="td"
                  sx={{ typography: "s3", py: 0.25, color: "text.secondary" }}
                >
                  {tool.action || COPY.noRoute}
                </Box>
                <Box component="td" sx={{ typography: "s3", py: 0.25 }}>
                  {BOUNDARY[tool.boundary] || COPY.notEnforced}
                </Box>
              </Box>
            ))}
          </Box>
        </Box>
      </Collapse>
    </Box>
  );
}

WorkerRow.propTypes = {
  worker: PropTypes.shape({
    worker_id: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    status: PropTypes.string.isRequired,
    reason_code: PropTypes.string,
    reason: PropTypes.string,
    tools: PropTypes.arrayOf(
      PropTypes.shape({
        tool: PropTypes.string,
        action: PropTypes.string,
        boundary: PropTypes.string,
      }),
    ).isRequired,
    bypassed: PropTypes.array,
    fix: PropTypes.shape({ action: PropTypes.string }),
  }).isRequired,
  dimmed: PropTypes.bool,
};

// One row per declared worker: its status, why, and each tool's boundary. Hidden when the contract declares none.
export default function WorkerBoundaries({ workers, dimmed = false }) {
  if (!workers?.length) return null;
  return (
    <Box component="section" aria-label={COPY.heading}>
      <Typography
        component="h3"
        sx={{
          typography: "s2",
          fontWeight: "fontWeightSemiBold",
          px: 1.5,
          pt: 1,
        }}
      >
        {COPY.heading}
      </Typography>
      {workers.map((worker) => (
        <WorkerRow key={worker.worker_id} worker={worker} dimmed={dimmed} />
      ))}
    </Box>
  );
}

WorkerBoundaries.propTypes = {
  workers: PropTypes.array,
  dimmed: PropTypes.bool,
};
